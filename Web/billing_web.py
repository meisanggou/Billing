#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
from flask import Flask, make_response
from flask_login import current_user
from Web import *

__author__ = 'zhouheng'


def create_app():
    flask_app = Flask("__name__")
    flask_app.secret_key = 'meisanggou'
    login_manager.init_app(flask_app)
    portal_url = dms_url_prefix + "/portal/"

    @flask_app.before_request
    def before_request():
        test_r, info = normal_request_detection(request.headers, request.remote_addr)
        if test_r is False:
            return make_response(info, 403)
        g.request_IP_s, g.request_IP = info
        g.portal_url = portal_url
        g.accept_json = False
        if "Accept" in request.headers:
            accept_content = request.headers["Accept"]
            if accept_content.startswith("application/json"):
                g.accept_json = True
        if current_user.is_authenticated:
            g.user_role = current_user.role
            g.user_name = current_user.user_name
            g.project_no = current_user.project_no
            g.project_name = current_user.project_name
            g.project_role = current_user.project_role
            if g.user_name in user_blacklist:
                message =u"不好意思，您的帐号存在异常，可能访问本系统出现不稳定的想象，现在就是不稳定中。本系统不是很智能，所以不知道啥时候会稳定，也许一分钟，也许一天，也许。。。"
                if "X-Requested-With" in request.headers:
                    return jsonify({"status": False, "data": message})
                return message
        else:
            g.user_role = 0

    @flask_app.after_request
    def after_request(res):
        if res.status_code == 302 or res.status_code == 301:
            if "X-Request-Protocol" in request.headers:
                pro = request.headers["X-Request-Protocol"]
                if "Location" in res.headers:
                    location = res.headers["location"]
                    if location.startswith("http:"):
                        res.headers["Location"] = pro + ":" + res.headers["Location"][5:]
                    elif location.startswith("/"):
                        res.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
        res.headers["Server"] = "JingYun Server"
        return res

    @flask_app.errorhandler(500)
    def handle_500(e):
        return str(e)

    flask_app.static_folder = "static2"
    flask_app.session_cookie_name = session_cookie_name
    if cookie_domain != "":
        flask_app.config.update(SESSION_COOKIE_DOMAIN=cookie_domain)
    flask_app.config.update(PERMANENT_SESSION_LIFETIME=60000)

    api_files = os.listdir("./views")
    for api_file in api_files:
        if api_file.endswith("_view.py"):
            __import__("Web.views.%s" % api_file[:-3])

    from Web import blues
    for key, value in blues.items():
        if len(value[1]) > 1:
            flask_app.register_blueprint(value[0], url_prefix=value[1])
        else:
            flask_app.register_blueprint(value[0])

    env = flask_app.jinja_env
    env.globals["current_env"] = current_env
    env.globals["role_value"] = control.role_value
    env.globals["menu_url"] = dms_url_prefix + "/portal/"
    env.filters['unix_timestamp'] = unix_timestamp
    env.filters['bit_and'] = bit_and
    env.filters['ip_str'] = ip_str
    env.filters['make_static_url'] = make_static_url
    env.filters['make_default_static_url'] = make_default_static_url
    env.filters['make_static_html'] = make_static_html
    return flask_app

msg_web = create_app()

for item in dms_job:
    item["max_instances"] = 10
    item["replace_existing"] = True
    dms_scheduler.add_job(**item)
dms_scheduler.start()


if __name__ == '__main__':
    print("start run")
    msg_web.run(port=2500)
