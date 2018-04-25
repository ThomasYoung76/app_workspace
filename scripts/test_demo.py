#coding: utf-8
"""
    调试
"""
import sys
sys.path.append('..')
from libs import *
import random
import string
import unittest
import time
from parameterized import parameterized
from BeautifulReport import BeautifulReport


class Demo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.sj = Fire_Compartment()
        # cls.sj = Controller()
        cls.sj = Linkage()

    def setUp(self):
        self.sj.driver.implicitly_wait(5)
        pass

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_programme_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    def test_linkage_400(self, index=7):
        """添加一条复合联动"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击复合联动
        self.sj.linkage_add(index)
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition_compound(host=2, loop=1, device_addr=3, is_add=True, save='confirm')
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn('right_click')
        # 选择设备类型、回路、区栋层
        self.sj.linkage_edit_output_result(loop='v2 (虚拟回路板)', community='1', building='1', index=[0, 1, 2], save='confirm')
        # 通过点击“编辑输入条件”进入“选择输入条件”界面，再取消退出
        self.sj.linkage_interface_choose_btn('edit_input')
        self.sj.linkage_edit_input_condition_compound(save='cancel')
        # 通过点击“编辑输出结果”进入“选择输出结果”界面，再取消退出
        self.sj.linkage_interface_choose_btn(button='edit_output')
        self.sj.linkage_edit_output_result(save='cancel')
        # 输出延时，去生效
        self.sj.linkage_interface_choose_btn(button='delay_spinner', delay=3, save='save_btn', is_effective=True)
        # 检查联动数正确
        count = self.sj.linkage_get_list_count()
        self.assertEqual(count, 1)
        # 获取当前页面生效联动数
        count_eff = self.sj.linkage_list_reg()[1]
        self.assertEqual(count_eff, 0)
        # 再次进入编辑，然后选择保存并继续添加
        self.sj.linkage_list_btn(list_value=[1, 'input'])
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition_compound(host=7, loop=2, device_addr=19, is_add=True, save='confirm')
        self.sj.linkage_interface_choose_btn(save='save_continue_add_btn')
        input_result = self.sj.linkage_get_input_condition()
        self.assertEqual(input_result[1], '条件相与')
        self.sj.linkage_interface_choose_btn(button='back_btn')
        result = self.sj.linkage_get_list_information()
        self.assertEqual(result[3][0], '7主机41回路板82回路19号')
        # 全部删除
        self.sj.linkage_list_btn('delete')
        self.sj.linkage_list_btn_confirm(True)


if __name__ == "__main__":
    # unittest.main(verbosity=2)
    run_suite(Demo)



