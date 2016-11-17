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
    return rt.render("new_member.html")


@project_view.route("/list/", methods=["GET"])
def list_member_func():
    return rt.render("list_member.html")
