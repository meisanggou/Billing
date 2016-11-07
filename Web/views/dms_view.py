#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from flask import request, render_template, redirect, session, url_for, jsonify, g, make_response
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from werkzeug.security import gen_salt
from Class.User import UserManager
from Web import User

from Web import dms_url_prefix, dev_url_prefix, api_url_prefix, bug_url_prefix, right_url_prefix
from Web import log_url_prefix, create_blue, param_url_prefix, release_url_prefix, status_url_prefix
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = dms_url_prefix

dms_view = create_blue('dms_view', url_prefix=url_prefix, auth_required=False)


user_m = UserManager()


@dms_view.route("/", methods=["GET"])
def index():
    next_url = ""
    if current_user.is_authenticated:
        if current_user.role == 0:
            return u"您还没有任何权限，请联系管理员授权"
        else:
            return redirect(url_prefix + "/portal/")
    if "X-Requested-With" in request.headers:
        if request.headers["X-Requested-With"] == "XMLHttpRequest":
            return make_response("登录状态已过期，需要重新登录", 302)
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
    # if info["tel"] is None:
    #     session["user_name"] = info["user_name"]
    #     session["bind_token"] = gen_salt(57)
    #     session["expires_in"] = datetime.now() + timedelta(seconds=300)
    #     session["password"] = password
    #     return redirect("%s/tel/" % url_prefix)
    if "remember" in request_data and request_data["remember"] == "on":
        remember = True
    else:
        remember = False
    user = User()
    user.user_name = info["user_name"]
    login_user(user, remember=remember)
    session["role"] = info["role"]
    if "next" in request_data and request_data["next"] != "":
        return redirect(request_data["next"])
    resp = redirect(url_prefix + "/portal/")
    return resp


@dms_view.route("/login/vip/", methods=["POST"])
def login_vip():
    request_data = request.json
    user_name = request_data["user_name"]
    result, info = user_m.check_vip(user_name)
    if result is False:
        return jsonify({"status": False, "data": "fail"})
    user = User()
    user.account = info["account"]
    login_user(user)
    session["role"] = info["role"]
    return jsonify({"status": True, "data": "success"})


@dms_view.route("/password/", methods=["GET"])
def password_page():
    if "user_name" in g:
        return render_template("password.html", url_prefix=url_prefix)
    elif "change_token" in session and "expires_in" in session and "user_name" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("password.html", user_name=session["user_name"],
                                   change_token=session["change_token"], url_prefix=url_prefix)
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["GET"])
def bind_tel_page():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("tel.html", user_name=session["user_name"],
                                   bind_token=session["bind_token"], url_prefix=url_prefix)
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["PUT"])
def send_tel_code():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            request_data = request.json
            bind_token = request_data["bind_token"]
            if bind_token != session["bind_token"]:
                return redirect(url_for("dms_view.login_page"))
            tel = request_data["tel"]
            result, info = control.send_code(session["user_name"], session["password"], tel)
            if result is True:
                session["tel"] = tel
                return jsonify({"status": True, "data": {"tel": tel}})
            return jsonify({"status": False, "data": info})
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["POST"])
def bind_tel_func():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            if "tel" not in session:
                return jsonify({"status": False, "data": "Please Send Code"})
            request_data = request.json
            bind_token = request_data["bind_token"]
            if bind_token != session["bind_token"]:
                return redirect(url_for("dms_view.login_page"))
            tel = request_data["tel"]
            if tel != session["tel"]:
                return jsonify({"status": False, "data": "Please Send Code First"})
            code = request_data["code"]
            user_name = session["user_name"]
            result, info = control.bind_tel(user_name, session["password"], tel, code)
            if result is True:
                user = User()
                user.account = user_name
                login_user(user)
                del session["bind_token"]
                del session["expires_in"]
                del session["user_name"]
                del session["password"]
                del session["tel"]
                return jsonify({"status": True, "data": {"tel": tel}})
            else:
                return jsonify({"status": False, "data": info})
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
    if g.user_role & control.role_value["user_new"] <= 0:
        return u"用户无权限操作"
    check_url = url_prefix + "/register/check/"
    return render_template("register.html", url_prefix=url_prefix, check_url=check_url, role_desc=control.user.role_desc)


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
    request_data = request.json
    check_name = request_data["check_name"]
    result, message = control.check_user_name_exist(current_user.account, current_user.role, check_name)
    if result is True:
        session["register_name"] = message
    return jsonify({"status": True, "data": {"result": result, "message": message}})


@dms_view.route("/authorize/", methods=["GET"])
@login_required
def authorize_page():
    result, my_user = control.get_my_user(current_user.account, current_user.role)
    if result is False:
        return my_user
    return render_template("authorize.html", my_user=my_user, url_prefix=url_prefix,
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
    return render_template("portal.html", api_url_prefix=api_url_prefix, dev_url_prefix=dev_url_prefix, bug_url_prefix=bug_url_prefix,
                           dms_url_prefix=dms_url_prefix, right_url_prefix=right_url_prefix,
                           log_url_prefix=log_url_prefix, param_url_prefix=param_url_prefix,
                           release_url_prefix=release_url_prefix, status_url_prefix=status_url_prefix)
