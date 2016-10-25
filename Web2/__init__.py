# encoding: utf-8
# !/usr/bin/python

__author__ = 'zhouheng'
import ConfigParser
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from Web2.redis_session import RedisSessionInterface
from Class.Control import ControlManager
from Class.User import UserManager

http_handlers = []

control = ControlManager()
user_m = UserManager()
ado_prefix = "/tornado"

api_url_prefix = ado_prefix + "/dev/api"
status_url_prefix = ado_prefix + "/dev/api/status"
test_url_prefix = ado_prefix + "/dev/api/test"
bug_url_prefix = ado_prefix + "/dev/bug"
right_url_prefix = ado_prefix + "/dev/right"
param_url_prefix = ado_prefix + "/dev/param"
dev_url_prefix = ado_prefix + "/dev"
dms_url_prefix = ado_prefix + ""
data_url_prefix = ado_prefix + "/data"
log_url_prefix = ado_prefix + "/log"
tools_url_prefix = ado_prefix + "/tools"
release_url_prefix = ado_prefix + "/dev/release"
github_url_prefix = ado_prefix + "/github"
chat_url_prefix = ado_prefix + "/chat"

import os

if os.path.exists("../env.conf") is False:
    current_env = "Development"

else:
    with open("../env.conf") as r_env:
        current_env = r_env.read().strip()

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

redis_host = config.get(current_env, "redis_host")
static_prefix_url = config.get(current_env, "static_prefix_url")
company_ip_start = config.getint(current_env, "company_ip_start")
company_ip_end = config.getint(current_env, "company_ip_end")
company_ips = [company_ip_start, company_ip_end]
cookie_domain = config.get(current_env, "cookie_domain")
session_id_prefix = config.get(current_env, "session_id_prefix")
session_cookie_name = config.get(current_env, "session_cookie_name")


def unix_timestamp(t, style="time"):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        if style == "time":
            return time.strftime('%H:%M:%S', x)
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", x)
    return t


def bit_and(num1, num2):
    return num1 & num2


def ip_str(ip_v):
    if type(ip_v) == int or type(ip_v) == long:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


def make_static_url(filename):
    return static_prefix_url + "/" + filename


def make_default_static_url(filename):
    return "/static/" + filename


def make_static_html(filename):
    src = make_static_url(filename)
    default_src = make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s


class GlobalInfo(object):
    def __init__(self):
        self.user_name = None
        self.user_role = 0


class TemplateRendering(object):
    """
    A simple class to hold methods for rendering templates.
    """

    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(self.settings['template_path'])
        env = Environment(loader=FileSystemLoader(template_dirs))
        env.globals["current_env"] = current_env
        env.globals["role_value"] = control.role_value
        env.filters['unix_timestamp'] = unix_timestamp
        env.filters['bit_and'] = bit_and
        env.filters['ip_str'] = ip_str
        env.filters['make_static_url'] = make_static_url
        env.filters['make_default_static_url'] = make_default_static_url
        env.filters['make_static_html'] = make_static_html
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


session_interface = RedisSessionInterface(redis_host, session_id_prefix, cookie_domain, session_cookie_name)


class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    route_url = ado_prefix

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.g = GlobalInfo()
        self.session = session_interface.open_session(self)
        if "user_role" in self.session:
            self.g.user_role = self.session["user_role"]
        if "user_name" in self.session:
            self.g.user_name = self.session["user_name"]
        self.kwargs = {"current_env": "Tornado " + current_env, "g": self.g, "role_value": user_m.role_value}

    def data_received(self, chunk):
        pass

    def current_user(self):
        if "user_name" in self.session and "user_role" in self.session:
            return self.session["user_name"]

    def render(self, template_name, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
        super(BaseHandler, self).render(template_name, **self.kwargs)

    def render_html(self, template_name, **kwargs):
        for key, value in kwargs.items():
            self.kwargs[key] = value
        self.kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'current_user': self.current_user,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **self.kwargs)
        self.write(content)

    def get_current_user(self):
        session_id = self.get_cookie("jydms")

    def save_session(self):
        session_interface.save_session(self)

    def on_finish(self):
        pass

    def finish(self, chunk=None):
        session_interface.save_session(self)
        super(BaseHandler, self).finish(chunk)


class BaseAuthHandler(BaseHandler):
    route_url = BaseHandler.route_url

    def prepare(self):
        super(BaseAuthHandler, self).prepare()
        if "user_name" not in self.session or "user_role" not in self.session:
            self.redirect(dms_url_prefix + "/login/?next=" + self.request.path)


class ErrorHandler(tornado.web.RequestHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    @tornado.web.addslash
    def prepare(self):
        if self._status_code == 404:
            if self.request.uri.startswith(ado_prefix):
                self.redirect(self.request.uri[len(ado_prefix):])
            else:
                self.write("Not Found")
            return
