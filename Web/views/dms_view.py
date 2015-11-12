#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Blueprint, request, render_template, redirect, session, url_for
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from Class.User import UserManager
from Class.Control import ControlManager
from Web import User

sys.path.append('..')

__author__ = 'Zhouheng'

dms_view = Blueprint('dms_view', __name__, url_prefix="/dms")


user_m = UserManager()
control = ControlManager()


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
    else:
        url_for_fun = "dms_view.select_channel"
    return url_for_fun


@dms_view.route("/", methods=["GET"])
def index():
    next_url = ""
    if current_user.is_authenticated():
        if current_user.role == 0:
            return u"您还没有任何权限，请联系管理员授权"
        else:
            return redirect(url_for(calc_redirect(current_user.role)))
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/login/", methods=["GET"])
def login_page():
    if current_user.is_authenticated():
        logout_user()
    next_url = ""
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/login/", methods=["POST"])
def login():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    result, message = user_m.check(user_name, password)
    if result is False:
        return message
    if "remember" in request_data and request_data["remember"] == "on":
        remember = True
    else:
        remember = False
    user = User()
    user.account = user_name
    login_user(user, remember=remember)
    session["role"] = message
    if "next" in request_data and request_data["next"] != "":
        return redirect(request_data["next"])
    if session["role"] == 0:
            return u"您还没有任何权限，请联系管理员授权"
    else:
        return redirect(url_for(calc_redirect(session["role"])))


@dms_view.route("/register/", methods=["GET"])
@login_required
def register_page():
    if current_user.role & control.user_role["user_new"] <= 0:
        return u"用户无权限操作"
    return render_template("register.html", user_role=current_user.role, role_value=control.user_role)


@dms_view.route("/register/", methods=["POST"])
@login_required
def register():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    nick_name = request_data["nick_name"]
    user_role = 0
    for key, value in user_m.role_value.items():
        if key in request_data and request_data[key] == "on":
            user_role += value
    result, message = control.new_user(user_name, password, user_role, nick_name, current_user.account, current_user.role)
    if result is False:
       return message
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/channel/", methods=["GET"])
@login_required
def select_channel():
    return render_template("Select_Channel.html", user_role=current_user.role, role_value=control.user_role)