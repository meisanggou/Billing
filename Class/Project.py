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

    def insert_user_project(self, user_name, project_no, project_role):
        join_time = int(time())
        kwargs = {"user_name": user_name, "project_no": project_no, "project_role": project_role,
                  "join_time": join_time}
        result = self.db.execute_insert(self.t_user_project, kwargs=kwargs, ignore=True)
        return result

    def insert_project_info(self, user_name, project_name, project_desc):
        project_no = uuid1().hex
        result = self.insert_user_project(user_name, project_no, 0)
        if result <= 0:
            return False
        create_time = int(time())
        p_info = {"project_no": project_no, "project_name": project_name, "project_desc": project_desc,
                  "create_time": create_time}
        self.db.execute_insert(self.t_project, kwargs=p_info)


if __name__ == "__main__":
    p_man = ProjectManager()
    p_man.insert_project_info("zh_test", "记账系统", "记账系统对外提供服务收费")