"""
    回路板设置
"""
import sys
sys.path.append('..')
from libs import *
import unittest


class Board(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sj = Controller()

    def setUp(self):
        pass

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/local_device_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    @classmethod
    def tearDownClass(cls):
        start_appium()

    def test_board_179_180(self):
        """单个回路板设置"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='device')
        self.sj.driver.find_element_by_name('回路板').click()
        # 注册3号回路板
        board_num = 3
        self.sj.app_device_loopboard(board_num, is_save=False)
        result = self.sj.app_get_device_loopboard(board_num)
        self.assertTrue(result.get('is_register'))
        # 取消注册3号回路板
        self.sj.app_device_loopboard(board_num, is_register=False, is_save=False)
        self.assertFalse(self.sj.app_get_device_loopboard(board_num).get('is_register'))
        # 保存设置
        self.sj.driver.find_element_by_name('保存').click()
        # 再进去检查3号回路板处于取消注册状态
        self.sj.app_menu(menu_id='device', is_click_menu=False)
        self.sj.driver.find_element_by_name('回路板').click()
        self.assertFalse(self.sj.app_get_device_loopboard(board_num).get('is_register'))
        # 返回菜单页

    def test_board_179_1(self):
        """批量回路板设置"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='device')
        self.sj.driver.find_element_by_name('回路板').click()
        # 批量注册3号到7号回路板(666,625)-> (1028,625)、(1028,625)
        self.sj.app_loopboard_batch_register(tap_loc=[(666, 625), (1028, 625), (1028, 625)])
        for board_num in range(3, 8):
            is_register = self.sj.app_get_device_loopboard(board_num=3)
            self.assertTrue(is_register.get('is_register'))
        # 批量去注册3号到7号回路板(666,625)-> (1028,625)、(1028,625) -> 取消
        self.sj.app_loopboard_batch_register(tap_loc=[(666, 625), (1028, 625), (1028, 625)], is_submit=False, is_register=False)
        for board_num in range(3, 8):
            result = self.sj.app_get_device_loopboard(board_num=3)
            self.assertTrue(result.get('is_register'))
        # 批量去注册3号到7号回路板(666,625)-> (1028,625)、(1028,625) -> 确定
        self.sj.app_loopboard_batch_register(tap_loc=[(666, 625), (1028, 625), (1028, 625)], is_register=False)
        for board_num in range(3, 8):
            is_register = self.sj.app_get_device_loopboard(board_num=3)
            self.assertFalse(is_register.get('is_register'))
        self.sj.app_device_loopboard(is_save=True)

    def test_board_183(self):
        """注册8号回路板，但8号回路板未接入，应能在100秒内报出“回路板通信故障”"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='device')
        self.sj.driver.find_element_by_name('回路板').click()
        # 注册8号回路，构造回路板通信故障
        board_num = 8
        self.sj.app_device_loopboard(board_num=board_num, is_register=True, is_save=True)
        sleep(30)  # 等待告警出现
        # 回到主页检查故障信息
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_main_page(ele_id='fault')
        raw_count = self.sj.app_main_page_get_notice(count_info=True)
        sleep(30)   # 等待告警出现
        result = self.sj.app_main_page_get_notice(get_notice_info=True)
        count = self.sj.app_main_page_get_notice(count_info=True)
        if int(count[-1]) != (int(raw_count[-1]) + 1):
            sleep(10)  # 告警仍未出现则再等待10秒
            result = self.sj.app_main_page_get_notice(get_notice_info=True)
            count = self.sj.app_main_page_get_notice(count_info=True)
        last_notice = result[-1]  # 最后一条记录
        last_notice.pop(-2)  # 去掉时间
        self.assertEqual(last_notice,
                         [count[-1], u'1号主机%d号回路板' % board_num, u'回路板通信故障', u'001-%d-000' % (board_num * 2 - 1)])
        # 去注册8号回路
        self.sj.app_menu(menu_id='device')
        self.sj.driver.find_element_by_name('回路板').click()
        self.sj.app_device_loopboard(board_num=board_num, is_register=False, is_save=True)
        self.sj.app_back_main_page()
        #  检查告警已恢复
        aim_count = self.sj.app_main_page_get_notice(count_info=True)
        self.assertEqual(raw_count, aim_count)


if __name__ == "__main__":
    # start_appium()
    # unittest.main(verbosity=2)
    run_suite(Board)
