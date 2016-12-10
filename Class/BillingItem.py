#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Tools.Mysql_db import DB


class ItemManager(object):

    def __init__(self):
        self.db = DB()
        self.t_item = "billing_item"

    def insert_item(self, project_no, item_no, item_name, unit_price, member_price):
        kwargs = dict(project_no=project_no, item_no=item_no, item_name=item_name, billing_method=1, billing_unit=1,
                      unit_price=unit_price, member_price=member_price)
        l = self.db.execute_insert(self.t_item, kwargs=kwargs, ignore=True)
        if l <= 0:
            return False, l
        return True, kwargs

    def new_item(self, project_no, item_name, unit_price=0, member_price=None, basic_item=None):
        unit_price *= 100
        if member_price is None:
            member_price = unit_price
        else:
            member_price *= 100
        where_value = dict(project_no=project_no)
        if basic_item is None:
            self.db.execute_select(self.t_item, where_value=where_value, cols=["MAX(item_no)"])
            max_no = self.db.fetchone()[0]
            if max_no is None:
                item_no = 100
            else:
                item_no = (max_no / 100 + 1) * 100
        else:
            basic_item = basic_item / 100 * 100
            next_basic_item = basic_item + 100
            where_cond = ["item_no >= %s" % basic_item, "item_no < %s" % next_basic_item]
            self.db.execute_select(self.t_item, where_value=where_value, cols=["MAX(item_no)"], where_cond=where_cond)
            max_no = self.db.fetchone()[0]
            if max_no is None:
                return False, "无效的主分类"
            item_no = max_no + 1
            if item_no >= next_basic_item:
                return False, "主分类下最多添加99个子分类"
        return self.insert_item(project_no, item_no, item_name, unit_price, member_price)

    def select_item(self, project_no):
        cols = ["item_no", "item_name", "billing_method", "billing_unit", "unit_price", "member_price"]
        db_items = self.db.execute_select(self.t_item, where_value={"project_no": project_no}, cols=cols, package=True)
        for item in db_items:
            item["unit_price"] /= 100.00
            item["member_price"] /= 100.00
        return True, db_items


if __name__ == "__main__":
    i_man = ItemManager()
    print i_man.new_item("d2747f52a64e11e6a69150af736dfb82", "项目", basic_item=703)[1]