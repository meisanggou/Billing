#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
import time
import os
import re
from flask import Flask, request, make_response, g, jsonify
from flask_login import current_user

from Web import login_manager
from Web import ip, env

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)


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
    else:
        g.user_role = 0


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
    # if "X-Requested-With" in request.headers and "Content-Type" in res.headers and res.status_code == 200:
    #     if request.headers["X-Requested-With"] == "XMLHttpRequest" and res.headers["Content-Type"] != "application/json":
    #         res = jsonify({"status": False, "data": res.response[0]})
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
static_prefix_url = "/static"
if env != "Development":
    msg_web.config.update(SESSION_COOKIE_DOMAIN="gene.ac")
    static_prefix_url = "http://static.gene.ac/dms_static"
msg_web.config.update(PERMANENT_SESSION_LIFETIME=600)


@msg_web.template_filter("make_static_url")
def make_static_url(filename):
    return static_prefix_url + "/" + filename


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

from Class.Log import LogManager
log = LogManager()
result, info = log.select_daily_log()
table_content = ""
for item in info["log_records"]:
    tr_content = '<tr title="info: %s&#10;host: %s">' % (item["info"].replace(">", "&gt;"), item["host"])
    tr_content += '<td name="run_begin" class="status_move">%s</td>\n' % unix_timestamp(item["run_begin"])
    tr_content += '<td name="request_url">%s</td>\n' % item["url"]
    tr_content += '<td>%s</td>' % item["method"]
    tr_content += '<td name="request_account">%s</td>\n' % item["account"]
    if item["level"] == "error":
        tr_content += '<td class="redBg">%s</td>' % item["level"]
    elif item["level"] == "base_error":
        tr_content += '<td class="orgBg">%s</td>' % item["level"]
    elif item["level"] == "bad_req":
        tr_content += '<td class="yellowBg">%s</td>' % item["level"]
    elif item["level"] == "http_error":
        tr_content += '<td class="greenBg">%s</td>' % item["level"]
    else:
        tr_content += '<td>%s</td>' % item["level"]
    tr_content += "\n"
    if item["run_time"] >= 1:
        tr_content += '<td class="redBg">%s</td>' % item["run_time"]
    elif item["run_time"] >= 0.5:
        tr_content += '<td class="orgBg">%s</td>' % item["run_time"]
    else:
        tr_content += '<td>%s</td>' % item["run_time"]
    tr_content += "\n"
    tr_content += '<td name="request_ip">%s</td>' % ip_str(item["ip"])
    tr_content += "\n"
    tr_content += '</tr>\n'
    table_content += tr_content

from Tools.MyEmail import MyEmailManager
my_email = MyEmailManager("/home/msg/conf/")
with open("../Web/templates/LOG/Daily_Log.html") as rt:
    content = rt.read()
    content = content.replace("{{ TR }}", table_content.encode("utf-8"))
    my_email.send_mail("zhouheng@gene.ac", u"运行日志", content)


if __name__ == '__main__':
    print("start run")
    msg_web.run(host="0.0.0.0", port=2200)
