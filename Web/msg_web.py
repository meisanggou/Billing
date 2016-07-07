#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
import time
import os
import re
from flask import Flask, request, make_response, g
from flask_login import current_user

# from Web.views.transport_view import transport_view as transport_view_blueprint
# from Web.views.develop_view import develop_view as develop_view_blueprint
# from Web.views.develop_api_view import develop_api_view as develop_api_view_blueprint
# from Web.views.develop_status_view import develop_status_view as develop_status_view_blueprint
# from Web.views.dms_view import dms_view as dms_blueprint
# from Web.views.develop_bug_view import develop_bug_view as bug_blueprint
# from Web.views.develop_right_view import develop_right_view as right_blueprint
# from Web.views.jy_log_view import jy_log_view as log_blueprint
# from Web.views.tools_view import tools_view as tools_blueprint
from Web import login_manager  #, data_url_prefix, dev_url_prefix, api_url_prefix, dms_url_prefix, bug_url_prefix
from Web import ip, env  #right_url_prefix, log_url_prefix, status_url_prefix, tools_url_prefix, ip, env

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)
# msg_web.register_blueprint(transport_view_blueprint, url_prefix=data_url_prefix)
# msg_web.register_blueprint(develop_view_blueprint, url_prefix=dev_url_prefix)
# msg_web.register_blueprint(develop_api_view_blueprint, url_prefix=api_url_prefix)
# msg_web.register_blueprint(develop_status_view_blueprint, url_prefix=status_url_prefix)
# msg_web.register_blueprint(dms_blueprint, url_prefix=dms_url_prefix)
# msg_web.register_blueprint(bug_blueprint, url_prefix=bug_url_prefix)
# msg_web.register_blueprint(right_blueprint, url_prefix=right_url_prefix)
# msg_web.register_blueprint(log_blueprint, url_prefix=log_url_prefix)
# msg_web.register_blueprint(tools_blueprint, url_prefix=tools_url_prefix)


@msg_web.template_filter('bit_and')
def bit_and(num1, num2):
    return num1 & num2


@msg_web.template_filter('unix_timestamp')
def unix_timestamp(t):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        return time.strftime('%H:%M:%S', x)
    return t

accept_agent = "(firefox|chrome|safari|window)"
trust_proxy = ["127.0.0.1", "10.25.244.32", "10.44.147.192"]


@msg_web.template_filter("ip_str")
def ip_str(ip_v):
    if type(ip_v) == int or type(ip_v) == long:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


@msg_web.template_filter("current_env")
def current_env(s):
    return env


@msg_web.before_request
def before_request():
    request_ip = request.remote_addr
    if "X-Forwarded-For" in request.headers:
        if request.remote_addr in trust_proxy:
            request_ip = request.headers["X-Forwarded-For"].split(",")[0]
    g.request_IP_s = request_ip
    g.request_IP = ip.ip_value_str(ip_str=request_ip)
    if g.request_IP == 0:
        return make_response(u"IP受限", 403)
    if "User-Agent" not in request.headers:
        print("No User-Agent")
        return make_response(u"请使用浏览器访问", 403)
    user_agent = request.headers["User-Agent"]
    if re.search(accept_agent, user_agent, re.I) is None:
        return make_response(u"浏览器版本过低", 403)
    if current_user.is_authenticated:
        g.user_role = current_user.role
        g.user_name = current_user.account


@msg_web.after_request
def after_request(res):
    if res.status_code == 302 or res.status_code == 301:
        if "X-Request-Protocol" in request.headers:
            pro = request.headers["X-Request-Protocol"]
            if "Location" in res.headers:
                location = res.headers["location"]
                if location.startswith("http"):
                    res.headers["Location"] = res.headers["Location"].replace("http", pro)
                else:
                    res.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
    res.headers["Server"] = "JingYun Server"
    return res


@msg_web.errorhandler(500)
def handle_500(e):
    return str(e)

# @msg_web.teardown_request
# def teardown_request(e=None):
#     print("enter teardown request")

msg_web.static_folder = "static2"
msg_web.session_cookie_name = "jydms"
if env != "Development":
    msg_web.config.update(SESSION_COOKIE_DOMAIN="gene.ac")
msg_web.config.update(PERMANENT_SESSION_LIFETIME=600)


api_files = os.listdir("./views")
for api_file in api_files:
    if api_file.endswith("_view.py"):
        exec "from Web.views import %s" % api_file[:-3]


from Web import blues
for key, value in blues.items():
    if len(value[1]) > 1:
        msg_web.register_blueprint(value[0], url_prefix=value[1])
    else:
        msg_web.register_blueprint(value[0])


if __name__ == '__main__':
    print("start run")
    msg_web.run(host="0.0.0.0", port=2200)
