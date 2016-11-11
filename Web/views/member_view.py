#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import g, jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, member_url_prefix as url_prefix, project_required
from Web import control


rt = RenderTemplate("member", url_prefix=url_prefix)
project_view = create_blue("project_view", url_prefix=url_prefix)


@project_view.route("/", methods=["GET"])
def project_info_func():
    if g.accept_json is True:
        p_info = control.get_project(g.user_name)
        return jsonify({"status": True, "data": p_info})
    return rt.render("new_member.html")
