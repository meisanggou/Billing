#! /usr/bin/env python
# coding: utf-8

import sys
from threading import Thread
from datetime import datetime
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from User import UserManager
from Member import MemberManager
from Project import ProjectManager
from BillingItem import ItemManager

__author__ = 'ZhouHeng'

my_email = MyEmailManager("/home/msg/conf/")


class ControlManager:

    def __init__(self):
        self.db = DB()
        self.sys_user = "sys_user"
        self.user = UserManager()
        self.user_role_desc = self.user.role_desc
        self.role_value = self.user.role_value
        self.pro_man = ProjectManager()
        self.member_man = MemberManager()
        self.item_man = ItemManager()

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

    # 针对项目的操作
    def get_project(self, user_name):
        return self.pro_man.get_project(user_name)

    def get_project_user(self, project_no, project_role):
        return self.pro_man.get_project_user(project_no)

    def new_project_info(self, user_name, user_role, project_name, project_desc):
        return self.pro_man.new_project_info(user_name, project_name, project_desc)

    def update_project_info(self, project_role, project_no, project_name, project_desc):
        return self.pro_man.update_project_info(project_no, project_name, project_desc)

    def new_project_grant(self, project_role, project_no, grant_info):
        return self.pro_man.insert_user_project(project_no, grant_info["user_name"], grant_info["project_role"])

    def update_project_grant(self, project_role, project_no, grant_info):
        return self.pro_man.update_project_info(project_no, grant_info["user_name"], grant_info["project_role"])

    def new_project_member(self, user_name, project_no, member_no):
        return self.pro_man.insert_project_member(project_no, member_no, user_name)

    # 会员相关
    def new_member(self, *args, **kwargs):
        return self.member_man.insert_member_info(*args, **kwargs)

    # 收费分类 相关
    def get_billing_items(self, project_no):
        return self.item_man.select_item(project_no)

    def new_item(self, *args, **kwargs):
        return self.item_man.new_item(*args, **kwargs)

