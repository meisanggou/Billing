#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Tools.RenderTemplate import RenderTemplate
from Web import create_blue, project_url_prefix as url_prefix
from Web import control


html_dir = "/Project"
rt = RenderTemplate("Project", url_prefix=url_prefix)
project_view = create_blue("project_view", url_prefix=url_prefix)


@project_view.route("/", methods=["GET"])
def project_info_func():
    return rt.render("project_info.html")
