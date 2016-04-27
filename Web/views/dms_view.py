#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from werkzeug.security import gen_salt
from Class.User import UserManager
from Web import User

from Web import dms_url_prefix, dev_url_prefix, api_url_prefix, bug_url_prefix, data_url_prefix, right_url_prefix
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = dms_url_prefix

dms_view = Blueprint('dms_view', __name__)


user_m = UserManager()


@dms_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


def calc_redirect(role):
    if role >= 1 and role <= 7:
        url_for_fun = "transport_view.show"
    elif role == 8 or role == 16 or role == 24:
        url_for_fun = "develop_api_view.list_api"
    elif role == 32:
        url_for_fun = "develop_view.show_data_table"
    elif role == 64:
        url_for_fun = "develop_view.operate_auth_show"
    elif role == 128:
        url_for_fun = "dms_view.register_page"
    elif role == 256 or role == 256 + 512:
        url_for_fun = "develop_bug_view.show_bug_list"
    else:
        url_for_fun = "dms_view.select_portal"
    return url_for_fun


@dms_view.route("/", methods=["GET"])
def index():
    next_url = ""
    if current_user.is_authenticated:
        if current_user.role == 0:
            return u"您还没有任何权限，请联系管理员授权"
        else:
            return redirect(url_for(calc_redirect(current_user.role)))
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url, url_prefix=url_prefix)


@dms_view.route("/login/", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        logout_user()
    next_url = ""
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url, url_prefix=url_prefix)


@dms_view.route("/login/", methods=["POST"])
def login():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    result, info = user_m.check(user_name, password)
    if result is False:
        return info
    if info["role"] == -1:
        session["user_name"] = info["account"]
        session["change_token"] = gen_salt(57)
        session["expires_in"] = datetime.now() + timedelta(seconds=300)
        session["password"] = password
        return redirect(url_for("dms_view.password_page"))
    if "remember" in request_data and request_data["remember"] == "on":
        remember = True
    else:
        remember = False
    user = User()
    user.account = info["account"]
    login_user(user, remember=remember)
    session["role"] = info["role"]
    if "next" in request_data and request_data["next"] != "":
        return redirect(request_data["next"])
    if session["role"] == 0:
            return u"您还没有任何权限，请联系管理员授权"
    else:
        return redirect(url_for(calc_redirect(session["role"])))


@dms_view.route("/password/", methods=["GET"])
def password_page():
    if current_user.is_authenticated:
        return render_template("password.html", user_name=current_user.account, url_prefix=url_prefix)
    elif "change_token" in session and "expires_in" in session and "user_name" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("password.html", user_name=session["user_name"],
                                   change_token=session["change_token"], url_prefix=url_prefix)
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/password/", methods=["POST"])
def password():
    user_name = request.form["user_name"]
    new_password= request.form["new_password"]
    confirm_password = request.form["confirm_password"]
    if new_password != confirm_password:
        return "两次输入密码不一致"
    if current_user.is_authenticated:
        old_password= request.form["old_password"]
        if old_password == new_password:
            return u"新密码不能和旧密码一样"
        result, message = control.change_password(user_name, old_password, new_password)
        if result is False:
            return message
        return redirect(url_for("dms_view.login_page"))
    elif "change_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            change_token = request.form["change_token"]
            if change_token != session["change_token"]:
                return "Bad change_token"
            if user_name != session["user_name"]:
                return "Bad user_name"
            result, message = control.change_password(user_name, session["password"], new_password)
            if result is False:
                return message
            del session["user_name"]
            del session["change_token"]
            del session["expires_in"]
            del session["password"]
            return redirect(url_for("dms_view.login_page"))
        else:
            return "更新密码超时，请重新登录"
    return "更新失败，请重新登录"


@dms_view.route("/register/", methods=["GET"])
@login_required
def register_page():
    if current_user.role & control.user_role_desc["user"]["role_list"]["user_new"]["role_value"] <= 0:
        return u"用户无权限操作"
    check_url = url_prefix + "/register/check/"
    return render_template("register.html", user_role=current_user.role, rl_prefix=url_prefix, check_url=check_url,
                           role_desc=control.user.role_desc)


@dms_view.route("/register/", methods=["POST"])
@login_required
def register():
    request_data = request.form
    user_name = request_data["user_name"]
    if "register_name" not in session or session["register_name"] != user_name:
        return u"页面已过期，请刷新重试"
    nick_name = request_data["nick_name"]
    user_role = 0
    for key, role_module in control.user.role_desc.items():
        for role_key, role_info in role_module["role_list"].items():
            if role_key in request.form and request.form[role_key] == "on":
                user_role += role_info["role_value"]
    result, message = control.new_user(user_name, user_role, nick_name, current_user.account, current_user.role)
    if result is False:
       return message
    return redirect(url_for("dms_view.select_portal"))


@dms_view.route("/register/check/", methods=["POST"])
@login_required
def register_check():
    request_data = request.form
    check_name = request_data["check_name"]
    result, message = control.check_user_name_exist(current_user.account, current_user.role, check_name)
    if result is True:
        session["register_name"] = message
    return jsonify({"status": result, "message": message})


@dms_view.route("/authorize/", methods=["GET"])
@login_required
def authorize_page():
    result, my_user = control.get_my_user(current_user.account, current_user.role)
    if result is False:
        return my_user
    return render_template("authorize.html", my_user=my_user, user_role=current_user.role, url_prefix=url_prefix,
                           role_desc=control.user.role_desc)


@dms_view.route("/authorize/user/", methods=["POST"])
@login_required
def authorize():
    perm_user = request.form["perm_user"]
    if perm_user == "":
        return "请选择一个账户"
    user_role = 0
    for key, role_module in control.user.role_desc.items():
        for role_key, role_info in role_module["role_list"].items():
            if role_key in request.form and request.form[role_key] == "on":
                user_role += role_info["role_value"]
    result, message = control.update_my_user_role(current_user.role, current_user.account, perm_user, user_role)
    if result is False:
        return message
    return redirect(url_for("dms_view.authorize_page"))


@dms_view.route("/portal/", methods=["GET"])
@login_required
def select_portal():
    return render_template("portal.html", user_role=current_user.role, data_url_prefix=data_url_prefix,
                           api_url_prefix=api_url_prefix, dev_url_prefix=dev_url_prefix, bug_url_prefix=bug_url_prefix,
                           dms_url_prefix=dms_url_prefix, right_url_prefix=right_url_prefix, role_desc=control.user_role_desc)


@dms_view.route("/user/email/", methods=["GET"])
@login_required
def test_send_email():
    if "X-Real-IP" in request.headers:
        request_IP = request.headers["X-Real-IP"]
    else:
        request_IP = request.remote_addr
    info = {"user_name": current_user.account, "request_ip": request_IP}
    content = u"尊敬的晶云文档系统使用者%(user_name)s:<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;您本次请求的IP为：%(request_ip)s<br /><br/ >"
    content += u"&nbsp;&nbsp;&nbsp;&nbsp;请求头部信息：<br />"
    for header in request.headers:
        content += "&nbsp;&nbsp;&nbsp;&nbsp;%s: %s<br />" % header
    content += str(request.headers)
    content = content % info
    result, email = control.test_send(current_user.account, content)
    if result is False:
        return email
    return u"已将测试邮件发送至%s，请注意查收。" % email