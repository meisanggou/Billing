# encoding: utf-8
# !/usr/bin/python

from datetime import datetime
from functools import wraps
from flask import session, g, redirect, Blueprint, jsonify, request
from flask_login import LoginManager, UserMixin, login_required
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from Class.Control import ControlManager
from Function.Common import *


__author__ = 'zhouheng'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

db = DB()
ip = IPManager()
control = ControlManager()
my_email = MyEmailManager("/home/msg/conf/")
dms_scheduler = BackgroundScheduler()


def err_listener(ev):
    with open("dms_task.log", "a") as wr:
        wr.write("----------%s----------\n" % datetime.now().strftime(TIME_FORMAT))
        if isinstance(ev, apscheduler.events.JobSubmissionEvent):
            wr.write("Job Submission Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
            wr.write("scheduled_run_times: %s\n" % ev.scheduled_run_times)
        elif isinstance(ev, apscheduler.events.JobExecutionEvent):
            wr.write("Job Execution Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
            wr.write("scheduled_run_time: %s\n" % ev.scheduled_run_time)
            print(ev.scheduled_run_time)
            wr.write("retval: %s\n" % ev.retval)
            wr.write("exception: %s\n" % ev.exception)
            wr.write("traceback: %s\n" % ev.traceback)
        elif isinstance(ev, apscheduler.events.JobEvent):
            wr.write("Job Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
        elif isinstance(ev, apscheduler.events.SchedulerEvent):
            wr.write("Scheduler Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("alias: %s\n" % ev.alias)
        wr.write("----------end----------\n")

dms_scheduler.add_listener(err_listener)


class User(UserMixin):
    user_name = ""

    def get_id(self):
        return self.user_name

login_manager = LoginManager()
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_name):
    user = User()
    user.user_name = user_name
    user.project_no = session["project_no"]
    if user.project_no is not None:
        user.project_name = session["project_name"]
        user.project_role = session["project_role"]
    user.role = session["role"]
    return user

login_manager.login_view = "dms_view.index"


dms_url_prefix = ""

project_url_prefix = "/project"
member_url_prefix = "/member"
billing_item_url_prefix = "/item"


blues = {}
dms_job = []


def create_blue(blue_name, url_prefix="/", auth_required=True):
    add_blue = Blueprint(blue_name, __name__)
    if auth_required:
        @add_blue.before_request
        @login_required
        def before_request():
            g.role_value = control.role_value

    @add_blue.route("/ping/", methods=["GET"])
    def ping():
        return jsonify({"status": True, "message": "ping %s success" % request.path})

    if blue_name not in blues:
        blues[blue_name] = [add_blue, url_prefix]
    return add_blue


def project_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "project_no" not in g or g.project_no is None:
            if g.accept_json is True:
                return jsonify({"status": False, "data": "未參加任何项目"})
            else:
                return redirect(g.portal_url)
        return f(*args, **kwargs)
    return decorated_function
