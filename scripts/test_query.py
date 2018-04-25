# coding: utf-8
"""
    记录查询
"""
import sys
sys.path.append('..')
from libs import *
import re
import unittest


class QueryRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sj = Controller()

    def setUp(self):
        self.sj.driver.implicitly_wait(5)

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_back_btn').click()
                flag = self.sj.app_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
                self.sj.app_main_page()
            except:
                pass

    def test_record_fault_133(self):
        """查询故障记录"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('query')
        self.sj.app_query('fault')
        self.sj.app_query_history('order', record_type='fault')
        self.sj.driver.find_element_by_name('按时间排序').click()
        records_raw = self.sj.app_query_history(record_num=0, record_type='fault')
        # 检查记录按时间逆序排列
        order_records = [x[1] for x in records_raw]
        # 将时间'2012-12-12 13:12'替换成整数201212121312
        sleep(2)
        int_time = [int(re.sub(r'\D', '', x)) for x in order_records]
        order_time = sorted(int_time, reverse=True)
        self.assertEqual(int_time, order_time)
        self.sj.app_query_history('order', record_type='fault')
        self.sj.driver.find_element_by_name('按调试码排序').click()
        # 检查记录按调试码排序
        records = self.sj.app_query_history(record_num=0, record_type='fault')
        order_debug_code = [x[-1] for x in records]
        int_code = [int(x.replace('-', '')) for x in order_debug_code]
        order_int_code = sorted(int_code)
        self.assertEqual(int_code, order_int_code)

    def test_record_fault_137(self):
        """检查故障记录的历史故障信息"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('query')
        self.sj.app_query('fault')
        record1 = self.sj.app_query_history(record_num=1, record_type='fault')
        self.sj.driver.find_element_by_name(record1[-1]).click()
        try:
            detail_title = self.sj.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/dialog_history_fault_detail_title').get_attribute('text')
            detail_code = self.sj.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/dialog_history_fault_detail_debug_code').get_attribute('text')
            detail_location = self.sj.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/dialog_history_fault_detail_location').get_attribute('text')
            detail_event = self.sj.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/history_fault_detail_event')[
                0].get_attribute('text')
            detail_time = self.sj.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/history_fault_detail_time')[
                0].get_attribute('text')
            self.assertEqual([detail_title, detail_code[1:-1], detail_location, detail_time, detail_event],
                             [u'历史故障', record1[-1], record1[3], record1[1], record1[4]])
        finally:
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_history_fault_detail_close').click()

    def test_record_fault_139(self):
        """故障记录清除"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('query')
        self.sj.app_query('fault')
        records_raw = self.sj.app_query_history(record_num=0, record_type='fault')
        self.sj.app_query_history('delete', record_type='fault')
        try:
            # 检查alert
            text = '此操作不可撤销，确认要删除所有故障记录吗？'
            self.assertTrue(self.sj.app_is_display(text))
        finally:
            # 点击取消后
            self.sj.driver.find_element_by_name('取消').click()
        records_cancel = self.sj.app_query_history(record_num=0, record_type='fault')
        self.assertEqual(len(records_raw), len(records_cancel))
        # 点击确定后，记录被删除
        self.sj.app_query_history('delete', record_type='fault')
        self.sj.driver.find_element_by_name('确定').click()
        records_delete = self.sj.app_query_history(record_num=0, record_type='fault')
        self.assertEqual(len(records_delete), 0)
        # 检查操作记录中新增“故障记录清除”的事件
        self.sj.app_query('operation')
        record = self.sj.app_query_history(record_num=1, record_type='operation')
        self.assertEqual(record[2], u'故障记录清除')

    def test_record_operation_140(self):
        """查询操作记录并排序"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('query')
        self.sj.app_query('operation')
        self.sj.app_query_history('order')
        self.sj.driver.find_element_by_name('按时间排序').click()
        records_raw = self.sj.app_query_history(record_num=0)
        # 检查记录按时间逆序排列
        order_records = [x[1] for x in records_raw]
        # 将时间'2012-12-12 13:12'替换成整数201212121312
        p = re.compile(r'\D')
        int_time = [int(p.sub('', x)) for x in order_records]
        order_time = sorted(int_time, reverse=True)
        self.assertEqual(int_time, order_time)
        self.sj.app_query_history('order')
        self.sj.driver.find_element_by_name('按用户排序').click()

    def test_record_operation_144(self):
        """操作记录清除"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('query')
        self.sj.app_query('operation')
        records_raw = self.sj.app_query_history(record_num=0)
        self.sj.app_query_history('delete')
        try:
            # 检查alert
            text = '此操作不可撤销，确认要删除所有操作记录吗？'
            self.assertTrue(self.sj.app_is_display(text))
        finally:
            # 点击取消后
            self.sj.driver.find_element_by_name('取消').click()
        records_cancel = self.sj.app_query_history(record_num=0)
        self.assertEqual(len(records_raw), len(records_cancel))
        # 点击确定后，记录被删除
        self.sj.app_query_history('delete')
        self.sj.driver.find_element_by_name('确定').click()
        records_delete = self.sj.app_query_history(record_num=0)
        self.assertEqual(len(records_delete), 1)


if __name__ == "__main__":
    # unittest.main(verbosity=2)
    run_suite(QueryRecord)

