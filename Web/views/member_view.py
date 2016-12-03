#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import g, jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, member_url_prefix as url_prefix, project_required
from Web import control


rt = RenderTemplate("member", url_prefix=url_prefix)
member_view = create_blue("member_view", url_prefix=url_prefix)


@member_view.route("/", methods=["GET"])
def page_new_member_func():
    return rt.render("new_member.html")


@member_view.route("/", methods=["POST"])
def new_member_func():
    request_data = request.json
    print(request_data)
    result, info = control.new_member(**request_data)
    return jsonify({"status": result, "data": info})


@member_view.route("/list/", methods=["GET"])
def list_member_func():
    return rt.render("list_member.html")
