#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os
from flask import render_template


class RenderTemplate(object):

    def __init__(self, template_dir="", **kwargs):
        self.template_dir = template_dir
        self.kwargs = kwargs

    def render(self, template_name_or_list, **context):
        if self.template_dir != "":
            template_name_or_list = os.path.join(self.template_dir, template_name_or_list)
        self.kwargs.update(context)
        return render_template(template_name_or_list, **self.kwargs)