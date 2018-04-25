# coding: utf-8
"""
    设备管理
"""
import sys
sys.path.append('..')
from libs import *
import unittest


class DeviceManage(unittest.TestCase):
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

    def test_device_manage_84(self):
        """单个手控盘注册\去注册"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        self.sj.app_local_device_handler(register_num=3)
        self.sj.app_local_device('save')
        # 回到主页复位
        self.sj.app_back_main_page()
        sleep(1)
        self.sj.app_main_page(text='复位')
        self.sj.driver.find_element_by_name('确定').click()
        sleep(5)
        # 检查注册成功
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        checkboxes = self.sj.driver.find_elements_by_class_name('android.widget.CheckBox')
        is_checked = checkboxes[3].get_attribute('checked')
        self.assertTrue(is_checked, 'true')
        # 去注册
        self.sj.app_local_device_handler(register_num=3)
        self.sj.app_local_device('save')
        # 回到主页复位
        self.sj.app_back_main_page()
        self.sj.app_main_page(text='复位')
        self.sj.driver.find_element_by_name('确定').click()
        sleep(5)
        # 检查去注册成功
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        checkboxes = self.sj.driver.find_elements_by_class_name('android.widget.CheckBox')
        is_checked = checkboxes[3].get_attribute('checked')
        self.assertTrue(is_checked, 'false')

    def test_device_manage_85(self):
        """批量注册\去注册所有的手控盘"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        self.sj.app_local_device_handler(is_batch_register=True)
        sleep(0.5)
        # 从="[548,484][570,530]"  号="[783,484][805,530]"  到="[908, 484][930, 530]"  号="[1148,484][1170,530]"
        self.sj.driver.tap([(1050, 458)])
        # sleep(1)
        # TouchAction(self.sj.driver).tap(x=1020, y=458)
        self.sj.app_handler_batch_register(is_register=True)
        self.sj.app_local_device('save')
        # 回到主页复位
        self.sj.app_menu(is_click_menu=False, is_click_back=True)
        self.sj.app_main_page(text='复位')
        self.sj.driver.find_element_by_name('确定').click()
        sleep(30)  # 等待30s，是为了等待首页上故障信息显示完成
        # 检查注册成功
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        checkboxes = self.sj.driver.find_elements_by_class_name('android.widget.CheckBox')
        for k in range(4):
            for i in range(8):
                self.assertEqual(checkboxes[i].get_attribute('checked'), 'true')
            self.sj.driver.swipe(1560, 800, 900, 367, 1000)
        # ------------------------去注册-----------------------------
        # 进入批量注册界面
        self.sj.app_local_device_handler(is_batch_register=True)
        # 从="[548,483][570,529]"  号="[783,483][805,529]"  到="[908, 483][930, 529]"  号="[1148,483][1170,529]"
        sleep(3)
        self.sj.driver.tap([(1050, 458)])
        # 去注册
        self.sj.app_handler_batch_register(is_register=False)
        self.sj.app_local_device('save')
        # 回到主页复位
        sleep(1)
        self.sj.app_menu(is_click_menu=False, is_click_back=True)
        self.sj.app_main_page(text='复位')
        self.sj.driver.find_element_by_name('确定').click()
        sleep(30)  # 等待30s，是为了等待首页上故障信息显示完成
        # 检查去注册成功
        self.sj.app_menu('device')
        self.sj.app_local_device('handler')
        checkboxes = self.sj.driver.find_elements_by_class_name('android.widget.CheckBox')
        for k in range(4):
            for i in range(8):
                self.assertEqual(checkboxes[i].get_attribute('checked'), 'false')
            self.sj.driver.swipe(1560, 800, 900, 367, 1000)

    def test_device_manage_86(self):
        """单个广播设备注册/去注册功能，并保存"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('device')
        self.sj.app_local_device('broadcast')
        self.sj.app_local_device_broadcast(7, point=60, is_register=True)
        try:
            # 在联动编程界面中检查
            self.sj.app_menu(is_click_menu=False, menu_id='linkage')
            self.sj.app_linkage_programme('add')
            self.sj.app_linkage_add('广播控制点设置')
            self.sj.app_linkage_add_broadcast(is_input=True)
            sleep(1)
            self.sj.app_linkage_add_broadcast_input(input_panel='7', input_point='1', is_submit=True)
            sleep(2)
        finally:
            # 回到菜单页
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_broadcast_back_btn').click()
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_programme_back_btn').click()
            # 去注册
            self.sj.app_menu(is_click_menu=False, menu_id='device')
            self.sj.app_local_device('broadcast')
            self.sj.app_local_device_broadcast(7, point=60, is_register=False)

    def test_device_manage_87(self):
        """广播控制盘设置不同点数正确"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('device')
        self.sj.app_local_device('broadcast')
        self.sj.app_local_device_broadcast(5, point=30, is_register=True)
        # 检查值为30点
        self.sj.app_menu(is_click_menu=False, menu_id='device')
        self.sj.app_local_device('broadcast')
        self.assertTrue(self.sj.app_local_device_broadcast_check_point(5, 30))
        # 注册为60点
        self.sj.app_local_device_broadcast(5, point=60, is_register=True)
        # 检查值为60点
        self.sj.app_menu(is_click_menu=False, menu_id='device')
        self.sj.app_local_device('broadcast')
        self.assertTrue(self.sj.app_local_device_broadcast_check_point(5, 60))
        # 选择90点注册
        self.sj.app_local_device_broadcast(5, point=90, is_register=True)
        # 检查值为90点
        self.sj.app_menu(is_click_menu=False, menu_id='device')
        self.sj.app_local_device('broadcast')
        self.assertTrue(self.sj.app_local_device_broadcast_check_point(5, 90))
        # 取消注册5号广播盘
        self.sj.app_local_device_broadcast(5, 30, is_register=False)


if __name__ == "__main__":
    # unittest.main(verbosity=2)
    run_suite(DeviceManage)
