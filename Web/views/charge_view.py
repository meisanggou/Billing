#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import g, jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, charge_url_prefix as url_prefix, project_required
from Web import control


rt = RenderTemplate("charge", url_prefix=url_prefix)
charge_view = create_blue("charge_view", url_prefix=url_prefix)


@charge_view.route("/", methods=["GET"])
def add_charge_page_func():
    return rt.render("charge_base.html")

