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
def add_billing_item_page_func():
    if g.accept_json is True:
        result, items_info = control.get_billing_items(g.project_no)
        return jsonify({"status": result, "data": items_info})
    action = "list"
    if "action" in request.args:
        action = request.args["action"]
    if action == "add":
        return rt.render("new_item.html")
    elif action == "update":
        return rt.render("update_item.html")
    return rt.render("list_item.html")

