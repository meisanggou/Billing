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
from APIHelp import HelpManager
from APIStatus import StatusManager
from Bug import BugManager
from Log import LogManager
from IP import IPManager
from Release import ReleaseManager
from ParamFormat import ParamFormatManager
from PullRequest import PullRequestManager
from Project import ProjectManager
from Class import DATE_FORMAT_STR, release_dir

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
        self.api_help = HelpManager()
        self.api_status = StatusManager()
        self.bug = BugManager()
        self.ip = IPManager()
        self.relase_man = ReleaseManager(release_dir)
        self.param_man = ParamFormatManager()
        self.pull_request_man = PullRequestManager()
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

    # 针对API HELP的应用
    def get_part_api(self, user_name, role):
        if role & self.role_value["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_part_api(user_name=user_name)

    def get_module_list(self, role):
        if role & self.role_value["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_module_list()

    def get_test_env(self, role, env_no_list=None):
        if role & self.role_value["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_test_env(env_no_list)

    def new_api_module(self, role, module_name, module_prefix, module_desc, module_part, module_env):
        if role & self.role_value["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_module(module_name, module_prefix, module_desc, module_part, module_env)

    def update_api_module(self, role, module_no, module_name, module_prefix, module_desc, module_part, module_env):
        if role & self.role_value["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.update_api_module(module_no, module_name, module_prefix, module_desc, module_part, module_env)

    def delete_api_module(self, role, module_no):
        if role & self.role_value["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_module(module_no)

    def new_api_info(self, module_no, title, path, method, desc, user_name, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, data = self.api_help.new_api_info(module_no, title, path, method, desc)
        if result is True:
            self.api_help.new_api_care(data["api_no"], user_name, 0)
            api_no = data["api_no"]
            t = Thread(target=self._send_module_message, args=(user_name, module_no, api_no, title, method, desc))
            t.start()
        return result, data

    def update_api_info(self, role, api_no, module_no, title, path, method, desc):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, data = self.api_help.update_api_info(api_no, module_no, title, path, method, desc)
        return result, data

    def get_api_info(self, api_no, role):
        if role & self.role_value["api_look"] <= 0:
            return False, u"您没有权限"
        result, api_info = self.api_help.get_api_info(api_no)
        if result is True:
            if role & self.role_value["api_new"] <= 0 and api_info["basic_info"]["stage"] == u'新建':
                return False, u"您没有权限"
        return result, api_info

    def add_header_param(self, user_name, api_no, param, necessary, desc, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_help.new_api_header(api_no, {param: {"necessary": necessary, "desc": desc}})
        if result is True:
            self._send_api_update_message_thread(user_name, api_no, param)
        return result, info

    def add_predefine_header(self, user_name, api_no, param, param_type, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_help.new_predefine_param(api_no, param, param_type)
        if result is True:
            self._send_api_update_message_thread(user_name, api_no, param)
        return result, info

    def add_body_param(self, user_name, api_no, param, necessary, type, desc, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_help.new_api_body(api_no, {param: {"necessary": necessary, "type": type, "desc": desc}})
        if result is True:
            self._send_api_update_message_thread(user_name, api_no, param)
        return result, info

    def add_input_example(self, user_name, api_no, example, desc, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_help.new_api_input(api_no, [{"desc": desc, "example": example}])
        if result is True:
            self._send_api_update_message_thread(user_name, api_no, u"请求示例")
        return result, info

    def add_output_example(self, user_name, api_no, example, desc, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_help.new_api_output(api_no, [{"desc": desc, "example": example}])
        if result is True:
            self._send_api_update_message_thread(user_name, api_no, u"返回示例")
        return result, info

    def add_care(self, api_no, user_name, role):
        if role & 8 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_care(api_no, user_name)

    def add_module_care(self, user_name, role, module_no):
        if role & 8 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_module_care(module_no, user_name)

    def get_api_list(self, module_no, role):
        if role & self.role_value["api_look"] <= 0:
            return False, u"您没有权限"
        result, api_list = self.api_help.get_api_list(module_no)
        if result is True and role & self.role_value["api_new"] <= 0:
            len_api = len(api_list["api_list"])
            for i in range(len_api - 1, -1, -1):
                api_item = api_list["api_list"][i]
                if api_item["stage"] == u'新建':
                    api_list["api_list"].remove(api_item)
        return result, api_list

    def delete_header(self, role, api_no, param):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_header(api_no, param)

    def delete_predefine_param(self, role, api_no, param):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_predefine_param(api_no, param)

    def delete_body(self, role, api_no, param):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_body(api_no=api_no, param=param)

    def delete_input(self, input_no, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_input(input_no)

    def delete_ouput(self, output_no, role):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_output(output_no)

    def delete_care(self, api_no, user_name):
        return self.api_help.del_api_care(api_no, user_name)

    def delete_module_care(self, user_name, module_no):
        return self.api_help.del_module_care(module_no, user_name)

    def delete_api(self, api_no, user_name):
        return self.api_help.del_api_info(api_no, user_name)

    def set_api_status(self, user_name, role, api_no, stage):
        if role & self.role_value["api_new"] <= 0:
            return False, u"您没有权限"
        if stage == 2:
            # 必须至少一个返回示例
            output_info = self.api_help.get_api_output(api_no)
            if len(output_info) <= 0:
                return False, u"请至少提交一个返回示例"
        result, info = self.api_help.set_api_stage(api_no, stage)
        return result, info

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

    # 针对BUG的应用
    def get_bug_list(self, role):
        if role & self.role_value["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_bug_list()

    def get_bug_statistic(self, role):
        if role & self.role_value["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_statistic()

    def get_bug_info(self, role, bug_no):
        if role & self.role_value["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_bug_info(bug_no)

    def new_bug(self, user_name, role, bug_title):
        if role & self.role_value["bug_new"] <= 0:
            return False, u"您没有权限"
        return self.bug.new_bug_info(bug_title, user_name)

    def add_bug_str_example(self, user_name, role, bug_no, content):
        if role & self.role_value["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断该bug是否是user_name提交的
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if submitter != user_name:
            return False, u"您不能修改别人的BUG"
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        return self.bug.new_bug_example(bug_no, 1, content)

    def add_bug_img_example(self, user_name, role, bug_no, path):
        if role & self.role_value["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断该bug是否是user_name提交的
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if submitter != user_name:
            return False, u"您不能修改别人的BUG"
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        return self.bug.new_bug_example(bug_no, 2, path)

    def _wx_send_bug(self, bug_no, user_name, type, link_desc):
        select_sql = "SELECT nick_name,wx_id,bug_title FROM %s as u,%s as b, %s as o " \
                     "WHERE u.user_name=o.user_name AND o.bug_no=b.bug_no " \
                     "AND type=%s AND u.user_name='%s' AND o.bug_no='%s';" \
                     % (self.user.user, self.bug.bug, self.bug.bug_owner, type, user_name, bug_no)
        result= self.db.execute(select_sql)
        if result != 0:
            nick_name, wx_id, bug_title = self.db.fetchone()
            if wx_id is not None:
                bug_url = "http://gene.ac/dev/bug/info?bug_no=%s" % bug_no
                title = u"%s, 您被标记为BUG %s" % (nick_name, link_desc)
                remark = u"请查看%s,如果是你的BUG，请尽快修复。" % bug_url
                pass

    def _wx_send_bug_thread(self, bug_no, user_name, type, link_desc):
        t = Thread(target=self._wx_send_bug, args=(bug_no, user_name, type, link_desc))
        t.start()

    def add_bug_link(self, bug_no, user_name, role, link_user, link_type):
        if role & self.role_value["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断当前bug是否允许添加关联者
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        # 判断被链接者是否可以被链接
        select_sql = "SELECT role FROM %s WHERE user_name='%s';" % (self.sys_user, link_user)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"添加关联账户不存在"
        link_role = self.db.fetchone()[0]
        if link_role & self.role_value["bug_link"] <= 0:
            return False, u"添加关联账户无效"
        if link_type == "ys":
            if bug_status > 1:
                return False, u"BUG 状态已不允许添加疑似拥有者"
            return self._add_ys_link(bug_no, user_name, link_user)
        elif link_type == "owner":
            return self._add_owner_link(bug_no, user_name, link_user, submitter)
        elif link_type == "fix":
            return self._add_fix_link(bug_no, user_name, link_user, submitter)
        elif link_type == "cancel":
            return self._add_channel_link(bug_no, user_name, role, link_user, submitter)
        elif link_type == "design":
            return self._add_design_link(bug_no, user_name, role, link_user)
        else:
            return False, u"错误的请求"

    def delete_bug_link(self, bug_no, user_name, role, link_user, link_type):
        if role & self.role_value["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断当前bug是否允许删除关联者
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        if link_type == "ys":
            if bug_status > 1:
                return False, u"BUG 状态已不允许修改疑似拥有者"
            link_type_num = 1
        elif link_type == "owner":
            link_type_num = 2
        else:
            return False, u"错误的请求"
        # 仅当当前关联者超过一个时才可以删除 其他
        select_sql = "SELECT user_name,adder FROM %s WHERE bug_no='%s' AND type=%s;" \
                     % (self.bug.bug_owner, bug_no, link_type_num)
        result = self.db.execute(select_sql)
        if result <= 1:
            return False, u"仅当关联者超过1个以后，才能删除"
        for item in self.db.fetchall():
            if item[0] == link_user and item[1] == user_name:
                return self.bug.del_bug_link(bug_no, link_user, link_type_num, user_name)
        return False, u"您无权限删除"

    def _add_ys_link(self, bug_no, user_name, link_user):
        # 有new bug的权限均可添加疑似bug拥有者
        result, info = self.bug.new_bug_link(bug_no, link_user, 1, user_name)
        if result is True:
            # 发送微信消息
            pass
        return result, info

    def _add_owner_link(self, bug_no, user_name, link_user, submitter):
        # 判断操作者是否有权限操作 操作者可以是关联自己 或者 是bug的提交者
        if user_name != link_user:
            # 判断提交者是否是bug提交者
            if submitter != user_name:
                return False, u"您不能修改别人的BUG"
        result, info = self.bug.new_bug_link(bug_no, link_user, 2, user_name)
        if result is True:
            # 发送微信消息
            pass
        return result, info

    def _add_fix_link(self, bug_no, user_name, link_user, submitter):
        # 只有BUG提交者可以标记为修复
        if submitter != user_name:
            return False, u"您不能修改别人的BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 3, user_name)

    def _add_channel_link(self, bug_no, user_name, role, link_user, submitter):
        # 只有bug提交者才 或者拥有bug_channel 权限的人可以操作
        if submitter != user_name and role & self.role_value["bug_cancel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 4, user_name)

    def _add_design_link(self, bug_no, user_name, role, link_user):
        # 拥有bug_channel 权限的人可以操作
        if role & self.role_value["bug_cancel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 5, user_name)

    # 发送API更新提醒
    def _send_module_message(self, user_name, module_no, api_no, title, method, desc):
        care_info = self.api_help.get_module_care_list(module_no=module_no)
        rec_user = []
        rec_email = []
        for care_user in care_info:
            if care_user["email"] is None:
                continue
            rec_user.append("%s|%s" % (care_user["user_name"], care_user["email"]))
            rec_email.append(care_user["email"])
        email_content_lines = []
        email_content_lines.append(u"模块增加新的API")
        email_content_lines.append(u"API标题：%s" % title)
        email_content_lines.append(u"API访问方法：%s" % method)
        email_content_lines.append(u"API描述：%s" % desc)
        access_url = "http://dms.gene.ac/dev/api/info/?api_no=%s" % api_no
        email_content_lines.append(u"<a href='%s'>查看详情</a>" % access_url)
        email_content = "<br/>".join(email_content_lines)
        # 写入更新信息
        self.api_help.new_send_message(user_name, rec_user, email_content)
        for email in rec_email:
            my_email.send_mail(email, u"模块增加新的API：%s" % title, email_content)

    def _send_api_update_message(self, user_name, api_no, param):
        result, api_info = self.api_help.get_api_basic_info(api_no)
        if result is False:
            return False
        # 判断添加api是否已完成
        if api_info["stage"] != 2:
            return False
        care_info = self.api_help.get_api_care_info(api_no)
        rec_user = []
        rec_email = []
        for care_user in care_info:
            if care_user["email"] is None:
                continue
            rec_user.append("%s|%s" % (care_user["user_name"], care_user["email"]))
            rec_email.append(care_user["email"])
        email_content_lines = []
        email_content_lines.append(u"API更新了参数")
        email_content_lines.append(u"API标题：%s" % api_info["api_title"])
        email_content_lines.append(u"API描述：%s" % api_info["api_desc"])
        email_content_lines.append(u"更新的参数名称：%s" % param)
        access_url = "http://dms.gene.ac/dev/api/info/?api_no=%s" % api_no
        email_content_lines.append(u"<a href='%s'>查看详情</a>" % access_url)
        email_content = "<br/>".join(email_content_lines)
        # 写入更新信息
        self.api_help.new_send_message(user_name, rec_user, email_content)
        for email in rec_email:
            my_email.send_mail(email, u"API:%s，更新了参数" % api_info["api_title"], email_content)
        return True

    def _send_api_update_message_thread(self, user_name, api_no, param):
        t = Thread(target=self._send_api_update_message, args=(user_name, api_no, param))
        t.start()

    def _send_api_completed_message(self, user_name, api_no):
        result, api_info = self.api_help.get_api_basic_info(api_no)
        if result is False:
            return False
        care_info = self.api_help.get_api_care_info(api_no)
        rec_user = []
        rec_email = []
        for care_user in care_info:
            if care_user["email"] is None:
                continue
            rec_user.append("%s|%s" % (care_user["user_name"], care_user["email"]))
            rec_email.append(care_user["email"])
        email_content_lines = []
        email_content_lines.append(u"API文档完成")
        email_content_lines.append(u"API标题：%s" % api_info["api_title"])
        email_content_lines.append(u"API描述：%s" % api_info["api_desc"])
        access_url = "http://dms.gene.ac/dev/api/info/?api_no=%s" % api_no
        email_content_lines.append(u"<a href='%s'>查看详情</a>" % access_url)
        email_content = "<br/>".join(email_content_lines)
        # 写入更新信息
        self.api_help.new_send_message(user_name, rec_user, email_content)
        for email in rec_email:
            my_email.send_mail(email, u"API:%s，文档已完成" % api_info["api_title"], email_content)
        return True

    def _send_api_completed_message_thread(self, user_name, api_no):
        t = Thread(target=self._send_api_completed_message, args=(user_name, api_no))
        t.start()

    def test_send(self, user_name, content):
        result, user_info = self.user.get_user_info(user_name)
        if result is False:
            return False, "user exception"
        if user_info["email"] is None:
            return False, "user not config email"
        my_email.send_mail_thread(user_info["email"], u"晶云文档系统测试发送与接收邮件", content)
        return True, user_info["email"]

    # 针对查看晶云平台运行日志
    def look_jy_log(self, user_name, role, start_time=None, end_time=None, level=None, search_url=None, search_account=None):
        if role & self.role_value["log_look"] <=0:
            return False, u"您没有权限"
        result, info = self.jy_log.show_log(start_time=start_time, end_time=end_time, level=level,
                                            search_url=search_url, search_account=search_account)
        return result, info

    def new_login_server(self, server_ip, server_name, user_ip, user_name, login_time):
        return self.jy_log.insert_login_server(server_ip, server_name, user_ip, user_name, login_time)

    def get_login_info(self):
        return self.jy_log.select_login_log()

    def register_log_task(self):
        return self.jy_log.register_daily_task()

    def get_daily_log(self):
        return self.jy_log.select_daily_log()

    def send_daily_log(self, template_html):
        result, user_list = self.user.get_role_user(self.role_value["log_receive"])
        subject = u"%s运行日志" % datetime.now().strftime(DATE_FORMAT_STR)
        if result is True:
            for u in user_list:
                my_email.send_mail(u["email"], subject, template_html)

    def register_login_task(self):
        return self.jy_log.register_login_task()

    # 针对工具
    def get_ip_info(self, ip_value):
        return self.ip.select_info_info(ip_value)

    # 针对发布
    def get_task(self, user_name, user_role):
        if user_role & self.role_value["release_ih_N"] <= 0:
            return False, u"您没有权限"
        return self.relase_man.select_release_task()

    def new_task(self, user_name, user_role, reason, restart_service, reason_desc):
        if user_role & self.role_value["release_ih_N"] <= 0 and user_name != "system":
            return False, u"您没有权限"
        if user_role & self.role_value["release_ih_V"] <= 0 and user_name != "system" and restart_service == 0:
            return False, u"您没有权限"
        if restart_service == 0:
            result, web_pull_requests = self.relase_man.select_web_pull_request()
            if len(web_pull_requests) <= 0:
                return False, u"WEB无更新不可提交"
            result, api_pull_requests = self.relase_man.select_api_pull_request()
            if len(api_pull_requests) <= 0:
                return False, u"API无更新不可提交"
        elif restart_service == 1:
            result, api_pull_requests = self.relase_man.select_api_pull_request()
            if len(api_pull_requests) <= 0:
                return False, u"API无更新不可提交"
        elif restart_service == 2:
            result, web_pull_requests = self.relase_man.select_web_pull_request()
            if len(web_pull_requests) <= 0:
                return False, u"WEB无更新不可提交"
        result, info = self.relase_man.select_release_task(user_name=user_name)
        if result is False:
            return False, info
        elif len(info) >= 2:
            return False, u"今日已不再允许预约"
        return self.relase_man.new_release_task(user_name, reason, restart_service, reason_desc)

    def update_task(self, release_no, run_result):
        return self.relase_man.update_release_task(release_no, run_result)

    def release_ih(self):
        return self.relase_man.release_ih()

    # 针对公共参数格式
    def add_param_format(self, user_name, user_role, param, param_type, **kwargs):
        return self.param_man.new_param_format(user_name, param, param_type, **kwargs)

    def update_param_format(self, user_name, user_role, param, **kwargs):
        return self.param_man.update_param_format(user_name, param, **kwargs)

    def get_params_info(self, user_name, user_role):
        return self.param_man.select_param_format()

    # 针对pull request
    def add_pull_request(self, **kwargs):
        return self.pull_request_man.add_pull_request(**kwargs)

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
