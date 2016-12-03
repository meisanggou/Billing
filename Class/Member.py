#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from uuid import uuid1
from time import time
from Tools.Mysql_db import DB


class MemberManager(object):

    def __init__(self):
        self.db = DB()
        pass

    def insert_member_info(self, card_no, member_name, member_sex, member_tel, member_birth, member_pwd, member_remark):
        member_no = uuid1().hex
        update_time = int(time())
        join_time = update_time
        kwargs = dict(member_no=member_no, card_no=card_no, member_name=member_name, member_sex=member_sex,
                      member_tel=member_tel, member_birth=member_birth, member_pwd=member_pwd,
                      member_remark=member_remark,join_time=join_time, update_time=update_time)
        self.db.execute_insert("member_info", kwargs=kwargs)
        return True, kwargs
