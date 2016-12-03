#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import g, jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, billing_item_url_prefix as url_prefix, project_required
from Web import control


rt = RenderTemplate("billingitem", url_prefix=url_prefix)
billing_item_view = create_blue("billing_item_view", url_prefix=url_prefix)


@billing_item_view.route("/", methods=["GET"])
def add_billing_item_page_func():
    return rt.render("new_item.html")