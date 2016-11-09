#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from time import time
from uuid import uuid1
from Tools.Mysql_db import DB


class ProjectManager:

    def __init__(self):
        self.db = DB()
        self.t_project = "project_info"
        self.t_user_project = "user_project"

    def insert_user_project(self, project_no, user_name, project_role):
        join_time = int(time())
        kwargs = {"user_name": user_name, "project_no": project_no, "project_role": project_role,
                  "join_time": join_time}
        result = self.db.execute_insert(self.t_user_project, kwargs=kwargs, ignore=True)
        return result

    def update_user_project(self, project_no, user_name, project_role):
        result = self.db.execute_update(self.t_user_project, update_value={"project_role": project_role},
                                        where_value={"user_name": user_name, "project_no": project_no})
        return result

    def new_project_info(self, user_name, project_name, project_desc):
        project_no = uuid1().hex
        result = self.insert_user_project(user_name, project_no, 0)
        if result <= 0:
            return False, "用户仅允许参加一个项目"
        create_time = int(time())
        p_info = {"project_no": project_no, "project_name": project_name, "project_desc": project_desc,
                  "create_time": create_time}
        self.db.execute_insert(self.t_project, kwargs=p_info)
        return True, p_info

    def update_project_info(self, project_no, project_name, project_desc):
        self.db.execute_update(self.t_project, update_value={"project_name": project_name, "project_desc": project_desc},
                               where_value={"project_no": project_no})
        return True

    def get_project(self, user_name):
        cols = ["project_no", "project_role", "join_time"]
        join_ps = self.db.execute_select(self.t_user_project, where_value={"user_name": user_name}, cols=cols,
                                        package=True)
        if len(join_ps) <= 0:
            return None
        my_project = join_ps[0]
        cols = ["project_name", "project_desc", "create_time"]
        p_info = self.db.execute_select(self.t_project, where_value={"project_no": my_project["project_no"]}, cols=cols,
                                        package=True)
        my_project.update(p_info[0])
        return my_project

    def get_project_user(self, project_no):
        cols = ["user_name", "project_role", "join_time"]
        members = self.db.execute_select(self.t_user_project, where_value={"project_no": project_no}, cols=cols,
                                         package=True)
        return True, members


if __name__ == "__main__":
    p_man = ProjectManager()
    p_man.new_project_info("zh_test", "记账系统", "记账系统对外提供服务收费")
    p_info = p_man.get_project("zh_test")
    print(p_info)
    print(p_man.get_project_user(p_info["project_no"]))