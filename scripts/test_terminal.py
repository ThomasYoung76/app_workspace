# coding: utf-8
"""
    终端设置
"""
import sys
sys.path.append('..')
from libs import *
import unittest


class Terminal(unittest.TestCase):
    user_num = 1
    user_password = '88888888'
    @classmethod
    def setUpClass(cls):
        cls.sj = Controller()
        # # ---------------构造初始数据--------------------
        # # 注册2号回路板
        # cls.sj.app_login(user_num=cls.user_num, password=cls.user_password)
        # cls.sj.app_menu('linkage_setting')
        # cls.sj.app_linkage_setting('interface_board')
        # cls.sj.app_device_loopboard(board_num=2, is_save=True)
        # # 进入终端设置，
        # cls.sj.app_linkage_setting('terminal')
        # # 设置1号回路板 1回路
        # cls.sj.app_terminal(loop_num=1)
        # sleep(5)
        # # 批量注册1到3号终端
        # cls.sj.app_terminal_setting_basic(terminal_num=(1, 4), is_batch=True, is_register=True)
        # # 批量屏蔽4、5号终端
        # cls.sj.app_terminal_setting_basic(terminal_num=(4, 6), is_batch=True, is_shield=True, is_save=True)
        # # 进入2回路板3回路
        # cls.sj.app_terminal(loop_num=3)
        # # 屏蔽且注册1号号
        # cls.sj.app_terminal_setting_basic(terminal_num=1, is_shield=True, is_register=True, is_save=True)

    # def tearDownClass(cls):
    #     # 取消注册2号回路板
    #     cls.sj.driver.find_element_by_name('返回')
    #     cls.sj.app_linkage_setting('interface_board')
    #     cls.sj.app_device_loopboard(board_num=2, is_register=False, is_save=True)

    def setUp(self):
        self.sj.driver.implicitly_wait(5)

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    def test_terminal_setting_01(self):
        """回路板注册后可以自动登录，取消注册后不能自动登录"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('device')
        self.sj.app_local_device('loopboard')
        # 注册回路板
        board_num = 2
        self.sj.app_device_loopboard(board_num=board_num, is_save=True, is_register=True)
        # 进入终端设置，检查回路板可以自动登录
        self.sj.app_menu('can_device', is_click_menu=False)
        result = self.sj.app_get_terminal(loop_num=board_num * 2 - 1)
        self.assertTrue(result[-1])
        result = self.sj.app_get_terminal(loop_num=board_num * 2)
        self.assertTrue(result[-1])
        # 取消注册回路板
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_back_btn').click()
        self.sj.app_menu('device', is_click_menu=False)
        self.sj.app_local_device('loopboard')
        self.sj.app_device_loopboard(board_num=board_num, is_save=True, is_register=False)

    def test_terminal_setting_216(self):
        """从详细设置界面返回上一个界面"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('can_device')
        self.sj.app_terminal(loop_num=1)
        loop_num = 1
        terminal_num = 101
        # 无修改下，点击返回
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_back_btn').click()
        sleep(1)
        self.sj.app_terminal(loop_num)
        self.sj.app_terminal_setting_basic(terminal_num, is_register=True)
        # 修改后点击返回
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_back_btn').click()
        text = '设置已经修改，是否保存？'
        self.assertTrue(self.sj.app_is_display(text))
        # 点击不保存
        self.sj.driver.find_element_by_name('不保存').click()
        # 检查没有保存
        self.sj.app_terminal(loop_num)
        result = self.sj.app_get_terminal_setting(terminal_num)
        self.assertFalse(result['is_register'])
        # 注册后返回再保存
        self.sj.app_terminal_setting_basic(terminal_num, is_register=True, is_shield=True)
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_back_btn').click()
        self.sj.driver.find_element_by_name('保存').click()
        # 检查保存生效
        self.sj.app_terminal(loop_num)
        result = self.sj.app_get_terminal_setting(terminal_num)
        self.assertTrue(result.get('is_register') and result.get('is_shield'))


if __name__ == "__main__":
    # start_appium()
    # unittest.main(verbosity=2)
    run_suite(Terminal)


