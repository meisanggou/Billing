#! /usr/bin/env python
# coding: utf-8

import sys
from threading import Thread
from datetime import datetime
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from User import UserManager
from Dev import DevManager
from APIStatus import StatusManager
from Log import LogManager
from IP import IPManager
from Project import ProjectManager

__author__ = 'ZhouHeng'

my_email = MyEmailManager("/home/msg/conf/")


class ControlManager:

    def __init__(self):
        self.db = DB()
        self.sys_user = "sys_user"
        self.user = UserManager()
        self.user_role_desc = self.user.role_desc
        self.role_value = self.user.role_value
        self.dev = DevManager()
        self.api_status = StatusManager()
        self.ip = IPManager()
        self.manger_email = ["budechao@ict.ac.cn", "biozy@ict.ac.cn"]
        self.jy_log = LogManager()
        self.pro_man = ProjectManager()

    def check_user_name_exist(self, user_name, role, check_user_name):
        if role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限新建用户"
        return self.user.check_account_exist(user_name, check_user_name)

    def new_user(self, user_name, role, nick_name, creator, creator_role):
        if creator_role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限新建用户"
        if creator_role | role > creator_role:
            return False, u"给新建用户赋予权限过高"
        return self.user.new(user_name, role, nick_name, creator)

    def change_password(self, user_name, old_password, new_password):
        return self.user.change_password(user_name, old_password, new_password)

    def send_code(self, user_name, password, tel):
        return self.user.send_code(user_name, password, tel)

    def bind_tel(self, user_name, password, tel, code):
        return self.user.bind_tel(user_name, password, tel, code)

    def get_my_user(self, user_name, role):
        if role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        return self.user.my_user(user_name)

    def update_my_user_role(self, role, user_name, my_user, my_user_role):
        if role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & my_user_role != my_user_role:
            return False, u"赋予权限过高"
        return self.user.update_my_user_role(my_user_role, my_user, user_name)

    def add_my_user_role(self, role, user_name, add_role, add_user_list):
        if role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & add_role != add_role:
            return False, u"增加权限过高"

        return self.user.add_role_my_users(add_role, add_user_list, user_name)

    def remove_my_user_role(self, role, user_name, remove_role, remove_user_list):
        if role & self.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & remove_role != remove_role:
            return False, u"移除权限过高"
        return self.user.remove_role_my_users(remove_role, remove_user_list, user_name)

    def get_role_user(self, role):
        return self.user.get_role_user(role)


    # 针对开发者的应用
    def show_operate_auth(self, role):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        return self.dev.get_operate_auth()

    def list_data_table(self, role):
        if role & self.role_value["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.list_table()

    def get_table_info(self, table_name, role):
        if role & self.role_value["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.get_table_info(table_name)

    def get_right_module(self, role):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_module()
        return result, info

    def get_right_module_role(self, role, module_no):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_module_role(module_no)
        return result, info

    def get_right_action_role(self, role, module_no):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_action_role(module_no)
        return result, info

    def new_right_action(self, user_name, role, module_no, action_desc, min_role):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        result, info = self.dev.new_right_action(module_no, action_desc, min_role, user_name)
        return result, info

    def delete_right_action(self, user_name, role, action_no):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        result, info = self.dev.del_right_action(user_name, action_no)
        return result, info

    def send_email(self, sub, data_no, info, attribute, attribute_ch):
        print("strart send email to %s" % self.manger_email)
        content = sub + "<br>"
        content += u"数据编号 : %s<br>" % data_no
        att_len = len(attribute)
        for index in range(att_len):
            content += "%s : %s<br>" % (attribute_ch[index], info[attribute[index]])
        for email in self.manger_email:
            my_email.send_mail_thread(email, sub, content)

    # 针对API状态码的应用
    def get_fun_info(self, role):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_function_info()

    def get_status(self, role):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_status_code()

    def get_error_type(self, role):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_error_type()

    def new_service_module(self, user_name, role, service_title, service_desc):
        if role & self.role_value["status_code_module"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_status.insert_service_module(service_title, service_desc)
        if result is False:
            return result, info
        service_id = info["service_id"]
        r, data = self.api_status.insert_function_module(service_id, u"公共功能模块", u"本服务模块所有功能模块可公共使用的错误状态码")
        if r is True:
            function_id = data["function_id"]
            error_info = [{"type_id": 0, "error_desc": u"访问系统正常，待用"},
                          {"type_id": 0, "error_desc": u"访问系统正常，将返回数据"},
                          {"type_id": 0, "error_desc": u"访问系统正常，仅返回成功信息"},
                          {"type_id": 0, "error_desc": u"访问系统正常，返回警告信息"},
                          {"type_id": 99, "error_desc": u"未经处理的异常，模块统一处理返回内部错误"}]
            r, data = self.api_status.new_mul_status_code(int(service_id), int(function_id), error_info, user_name)
        return result, info

    def new_function_module(self, user_name, role, service_id, function_title, function_desc):
        if role & self.role_value["status_code_module"] <= 0:
            return False, u"您没有权限"
        return self.api_status.insert_function_module(service_id, function_title, function_desc)

    def new_api_status(self, user_name, role, service_id, fun_id, type_id, error_id, error_desc):
        if role & self.role_value["status_code_new"] <= 0:
            return False, u"您没有权限"
        return self.api_status.new_status_code(service_id, fun_id, type_id, error_id, error_desc, user_name)

    def new_mul_api_status(self, user_name, role, service_id, fun_id, error_info):
        if role & self.role_value["status_code_new"] <= 0:
            return False, u"您没有权限"
        return self.api_status.new_mul_status_code(service_id, fun_id, error_info, user_name)

    def delete_api_status(self, user_name, role, status_code):
        if role & self.role_value["status_code_del"] < self.role_value["status_code_del"]:
            return False, u"您没有权限"
        return self.api_status.del_status_code(status_code)

    # 针对项目的操作
    def get_project(self, user_name):
        return self.pro_man.get_project(user_name)

    def get_project_user(self, project_no, project_role):
        return self.pro_man.get_project_user(project_no)

    def new_project_info(self, user_name, user_role, project_name, project_desc):
        return self.pro_man.new_project_info(user_name, project_name, project_desc)

    def update_project_info(self, project_role, project_no, project_name, project_desc):
        return self.pro_man.update_project_info(project_no, project_name, project_desc)

    def new_project_member(self, project_role, project_no, member_info):
        return self.pro_man.insert_user_project(project_no, member_info["user_name"], member_info["project_role"])

    def update_project_member(self, project_role, project_no, member_info):
        return self.pro_man.update_project_info(project_no, member_info["user_name"], member_info["project_role"])
