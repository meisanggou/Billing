#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
sys.path.append("..")
from datetime import datetime, timedelta
from Tools.Mysql_db import DB
from Class import table_manager, TIME_FORMAT
from Check import check_sql_character

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class BugManager:

    def __init__(self):
        self.db = DB()
        self.bug = table_manager.bug
        self.bug_owner = table_manager.bug_owner
        self.bug_example = table_manager.bug_example
        self.user = "sys_user"

    def new_bug_info(self, bug_title, submitter):
        submit_time = datetime.now().strftime(TIME_FORMAT)
        bug_no = uuid.uuid1().hex
        if len(bug_title) < 5:
            return False, "Bad bug_title"
        bug_title = check_sql_character(bug_title)[:50]
        insert_sql = "INSERT INTO %s (bug_no,bug_title,submitter,submit_time) VALUES ('%s','%s','%s','%s');" \
                     % (self.bug, bug_no, bug_title, submitter, submit_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"bug_no": bug_no, "bug_title": bug_title, "submitter": submitter, "submit_time": submit_time}

    def new_bug_link(self, bug_no, user_name, link_type, adder):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        link_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (bug_no,user_name,type,link_time,adder) VALUES ('%s','%s','%s','%s','%s') " \
                     "ON DUPLICATE KEY UPDATE adder=adder;" \
                     % (self.bug_owner, bug_no, user_name, link_type, link_time, adder)
        result = self.db.execute(insert_sql)
        # if result != 1:
        #     return False, "sql execute result is %s " % result
        self.update_bug_status(bug_no, link_type)
        return True, {"bug_no": bug_no, "user_name": user_name, "link_type": link_type, "link_time": link_time}

    def del_bug_link(self, bug_no, user_name, link_type, adder):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        delete_sql = "DELETE FROM %s WHERE bug_no='%s' AND user_name='%s' AND adder='%s' AND type=%s;" \
                     % (self.bug_owner, bug_no, user_name, adder, link_type)
        result = self.db.execute(delete_sql)
        return True, result

    def new_bug_example(self, bug_no, example_type, content):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        add_time = datetime.now().strftime(TIME_FORMAT)
        if len(content) < 5:
            return False, "Bad content"
        content = check_sql_character(content)
        insert_sql = "INSERT INTO %s (bug_no,type,content,add_time) VALUES ('%s','%s','%s','%s');" \
                     % (self.bug_example, bug_no, example_type, content, add_time)
        result = self.db.execute(insert_sql)
        if result != 1:
            return False, "sql execute result is %s " % result
        return True, {"bug_no": bug_no, "example_type": example_type, "content": content, "add_time": add_time}

    def update_bug_status(self, bug_no, status):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        update_sql = "UPDATE %s SET bug_status=%s WHERE bug_no='%s';" % (self.bug, status, bug_no)
        result = self.db.execute(update_sql)
        return True, result

    def get_bug_list(self, offset=0, num=20):
        if type(offset) != int or type(num) != int:
            return False, "Bad offset or num"
        select_sql = "SELECT bug_no,bug_title,submitter,submit_time,bug_status FROM %s " \
                     "ORDER BY bug_status,submit_time DESC LIMIT %s, %s;" % (self.bug, offset, num)
        self.db.execute(select_sql)
        bug_list = []
        for item in self.db.fetchall():
            bug_list.append({"bug_no": item[0], "bug_title": item[1], "submitter": item[2],
                             "submit_time": item[3].strftime(TIME_FORMAT), "bug_status": item[4]})
        return True, bug_list

    def get_bug_info(self, bug_no):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        # 获取基本信息
        select_sql = "SELECT bug_no,bug_title,submitter,submit_time,bug_status,nick_name FROM %s AS i,%s AS u " \
                     "WHERE bug_no='%s' AND i.submitter=u.user_name;" \
                     % (self.bug, self.user, bug_no)
        result = self.db.execute(select_sql)
        if result != 1:
            return False, "Bad bug_no."
        info = self.db.fetchone()
        basic_info = {"bug_no": info[0], "bug_title": info[1], "submitter": info[2],
                      "submit_time": info[3].strftime(TIME_FORMAT), "bug_status": info[4], "submit_name": info[5]}
        # 获取示例信息
        select_sql = "SELECT type,content,add_time FROM %s WHERE bug_no='%s' ORDER BY add_time;" % (self.bug_example, bug_no)
        self.db.execute(select_sql)
        example_info = []
        for item in self.db.fetchall():
            example_info.append({"example_type": item[0], "content": item[1], "add_time": item[2].strftime(TIME_FORMAT)})
        # 获取关联的人
        select_sql = "SELECT o.user_name,type,link_time,adder,nick_name FROM %s AS o, %s AS u " \
                     "WHERE bug_no='%s' AND o.user_name=u.user_name;" % (self.bug_owner, self.user, bug_no)
        self.db.execute(select_sql)
        link_user = {"ys": {}, "owner": {}, "fix": {}, "channel": {}, "design": {}}
        for item in self.db.fetchall():
            link_info = {"user_name": item[0], "link_type": item[1], "link_time": item[2].strftime(TIME_FORMAT),
                         "adder": item[3], "nick_name": item[4]}
            if item[1] == 1:
                link_user["ys"][item[0]] = link_info
            elif item[1] == 2:
                link_user["owner"][item[0]] = link_info
            elif item[1] == 3:
                link_user["fix"][item[0]] = link_info
            elif item[1] == 4:
                link_user["channel"][item[0]] = link_info
            elif item[1] == 5:
                link_user["design"][item[0]] = link_info
            else:
                pass
        return True, {"basic_info": basic_info, "example_info": example_info, "link_user": link_user}

    def get_statistic(self):
        # 获得所有的统计信息
        bug_role = 1024
        select_sql = "SELECT u.user_name,nick_name,count(bug_no) AS bug_num FROM %s as u LEFT JOIN %s as b " \
                     "on u.user_name=b.user_name AND type=2 WHERE role & %s = %s " \
                     "GROUP BY u.user_name ORDER BY bug_num DESC;" \
                     % (self.user, self.bug_owner, bug_role, bug_role)
        self.db.execute(select_sql)
        all_data = []
        for item in self.db.fetchall():
            all_data.append({"user_name": item[0], "nick_name": item[1], "bug_num": item[2]})
        # 获得最近一个月的统计信息
        after_time = (datetime.now() - timedelta(days=30)).strftime(TIME_FORMAT)
        select_sql = "SELECT u.user_name,nick_name,count(bug_no) AS bug_num FROM %s as u LEFT JOIN %s as b " \
                     "on u.user_name=b.user_name AND type=2 AND link_time>'%s' " \
                     "WHERE role & %s = %s GROUP BY u.user_name ORDER BY bug_num DESC;" \
                     % (self.user, self.bug_owner, after_time, bug_role, bug_role)
        self.db.execute(select_sql)
        month_data = []
        for item in self.db.fetchall():
            month_data.append({"user_name": item[0], "nick_name": item[1], "bug_num": item[2]})
        return True, {"month": month_data, "all": all_data}