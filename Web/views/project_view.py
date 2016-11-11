#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import g, jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, project_url_prefix as url_prefix, project_required
from Web import control


rt = RenderTemplate("project", url_prefix=url_prefix)
project_view = create_blue("project_view", url_prefix=url_prefix)


@project_view.route("/", methods=["GET"])
def project_info_func():
    if g.accept_json is True:
        p_info = control.get_project(g.user_name)
        return jsonify({"status": True, "data": p_info})
    return rt.render("project_info.html")


@project_view.route("/", methods=["POST"])
def new_project_func():
    request_data = request.json
    project_name = request_data["project_name"]
    project_desc = request_data["project_desc"]
    result, msg = control.new_project_info(g.user_name, g.user_role, project_name, project_desc)
    if result is True:
        return jsonify({"status": True, "location": g.portal_url, "data": "success"})
    return jsonify({"status": result, "data": msg})


@project_required
@project_view.route("/", methods=["PUT"])
def update_project_func():
    request_data = request.json
    project_desc = request_data["project_desc"]
    result, msg = control.update_project_info(g.project_role, g.project_no, g.project_name, project_desc)
    if result is True:
        return jsonify({"status": True, "location": g.portal_url, "data": "success"})
    return jsonify({"status": result, "data": msg})