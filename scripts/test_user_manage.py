# coding: utf-8
"""
    测试用户管理
"""
import sys
sys.path.append('..')
from libs import *
from parameterized import parameterized
import random
import string
import unittest


class UserManage(unittest.TestCase):

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
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    def test_user_manage_52(self):
        """用户名字符长度为8，支持空格，特殊字符"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        # 用户名合法
        for user_name in ['6', 'abc1 dd4', 'ai1']:
            self.sj.app_setting_user(is_add=True)
            is_added = self.sj.app_add_user(name=user_name, type='调试员', password='12345678', password_again='12345678')
            self.assertTrue(is_added)
            if is_added:
                self.sj.app_setting_user(user_name=user_name)
                self.sj.app_edit_user('delete_btn')
                self.sj.driver.find_element_by_name('确定').click()

    def test_user_manage_53(self):
        """用户名不合法"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)

        user_name0 = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(
            random.randint(0, 100))
        self.sj.app_add_user(name=user_name0, type='调试员', password='12345678', password_again='12345678')
        try:
            # 用户名不合法（空，重名）
            self.sj.app_setting_user(is_add=True)
            for user_name in ['', ' ', user_name0]:
                is_added = self.sj.app_add_user(name=None, type='值班管理员', password='123456', password_again='123456')
                self.assertFalse(is_added)
            # 不设置密码
            is_added = self.sj.app_add_user(name='1240as', type='值班员')
            self.assertFalse(is_added)
        finally:
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_back_btn').click()
            self.sj.app_setting_user(user_name=user_name0)
            self.sj.app_edit_user('delete_btn')
            self.sj.driver.find_element_by_name('确定').click()

    @parameterized.expand(input=params_sys+params_adj)
    def test_user_manage_54(self, name, user_num, password):
        """添加用户时可选择的用户类型"""
        user = self.sj.app_login(user_num=user_num, password=password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        self.assertTrue(self.sj.app_is_display('值班员'))
        if user['type'] == '系统管理员':
            self.assertFalse(self.sj.app_is_display('系统管理员'))
            self.assertTrue(self.sj.app_is_display('调试员'))
            self.assertTrue(self.sj.app_is_display('值班管理员'))
        elif user['type'] == '调试员':
            self.assertFalse(self.sj.app_is_display('调试员'))
            self.assertTrue(self.sj.app_is_display('值班管理员'))
        elif user['type'] == '值班管理员':
            self.assertFalse(self.sj.app_is_display('系统管理员'))
            self.assertFalse(self.sj.app_is_display('调试员'))
            self.assertFalse(self.sj.app_is_display('值班管理员'))
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_back_btn').click()

    def test_user_manage_55(self):
        """添加用户设置密码功能测试"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        user_name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(
            random.randint(0, 9)) + random.choice(string.ascii_letters)
        # 两次输入密码不一致
        self.sj.app_add_user(name=user_name, type='调试员',password='11114444', password_again='11114445', is_save=False)
        text = "两次输入的密码不一致，请重新输入"
        self.assertTrue(self.sj.app_is_display(text))
        try:
            # 重新输入密码一致
            self.sj.app_input_password(22222222)
            self.sj.app_input_password(22222222)
            text = '已完成密码设置'
            self.assertTrue(self.sj.app_is_display(text))
            # 修改密码
            self.sj.app_add_user(name=None, type=None, password='87654321', password_again='87654321', is_save=True)
        finally:
            # 删除用户
            sleep(1)
            self.sj.driver.find_element_by_name(user_name).click()
            self.sj.app_edit_user('delete_btn')
            self.sj.driver.find_element_by_name('确定').click()

    def test_user_manage_56(self):
        """自动注销时间11分钟"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        user_name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(
            random.randint(0, 9))
        self.sj.app_add_user(name=user_name, type='调试员', password='11114444', password_again='11114444', time_tx=11)
        # 使用新增用户登录，验证自动注销时间
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
        self.sj.app_login(user_name=user_name, password='11114444')
        sleep(60 * 11 + 5)
        # appium重新连接服务器(appium在1分钟无操作后自动退出)
        self.setUpClass()
        self.assertTrue(self.sj.app_is_display('登录'))
        # 使用系统管理员登录，删除新增用户
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(user_name=user_name)
        self.sj.app_edit_user('delete_btn')
        self.sj.driver.find_element_by_name('确定').click()

    @parameterized.expand(input=params_raw)
    def test_user_manage_57(self, name, user_num, password):
        """观察不同等级用户可以编辑的用户类型"""
        user = self.sj.app_login(user_num=user_num, password=password)
        self.sj.app_menu('user')
        user_types = self.sj.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userType')
        if user['type'] == '系统管理员':
            self.assertTrue('系统管理员' == user_types[0].get_attribute('text'))
            self.assertTrue('调试员' == user_types[1].get_attribute('text'))
            self.assertTrue('值班管理员' == user_types[2].get_attribute('text'))
            self.assertTrue('值班员' == user_types[3].get_attribute('text'))
        elif user['type'] == '调试员':
            self.assertTrue('调试员' == user_types[0].get_attribute('text'))
            self.assertTrue('值班管理员' == user_types[1].get_attribute('text'))
            self.assertTrue('值班员' == user_types[2].get_attribute('text'))
        elif user['type'] == '值班管理员':
            self.assertTrue('值班管理员' == user_types[0].get_attribute('text'))
            self.assertTrue('值班员' == user_types[1].get_attribute('text'))

    def test_user_manage_58(self):
        """修改现有用户密码"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(user_num=1)
        # 修改密码
        self.sj.app_edit_user('change_password_btn')
        # 两次输入的密码不一致
        self.sj.app_input_password('12345123')
        self.sj.app_input_password('12345133')
        text = '两次输入的密码不一致，请重新输入'
        self.assertTrue(self.sj.app_is_display(text))
        # 两次输入的密码一致
        new_password = '12345188'
        self.sj.app_input_password(new_password)
        self.sj.app_input_password(new_password)
        text = '密码修改成功，请妥善保管新密码!'
        self.assertTrue(self.sj.app_is_display(text))
        # 回到主页
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_close').click()
        self.sj.driver.find_element_by_id('user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_login(user_num=user_num, password=new_password)
        # 还原密码
        self.sj.app_menu('user')
        self.sj.app_setting_user(user_num=1)
        # 修改密码
        self.sj.app_edit_user('change_password_btn')
        self.sj.app_input_password(user_password)
        self.sj.app_input_password(user_password)
        text = '密码修改成功，请妥善保管新密码!'
        self.assertTrue(self.sj.app_is_display(text))
        # 回到主页
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_close').click()
        self.sj.driver.find_element_by_id('user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()

    def test_user_manage_59(self):
        """增加用户1后删除用户1，再增加用户1。 mantis:0001053"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        # 增加用户并删除
        user_name = 'abcdefgs'
        newpassword = '12345671'
        self.sj.app_add_user(name=user_name, type='调试员', password=newpassword, password_again=newpassword, is_save=True)
        self.sj.driver.find_element_by_name(user_name).click()
        self.sj.app_edit_user('delete_btn')
        self.sj.driver.find_element_by_name('确定').click()
        # 再次增加同名用户成功
        self.sj.app_setting_user(is_add=True)
        self.sj.app_add_user(name=user_name, type='调试员', password=newpassword, password_again=newpassword, is_save=True)
        # 还原环境，清除该用户
        self.sj.driver.find_element_by_name(user_name).click()
        self.sj.app_edit_user('delete_btn')
        self.sj.driver.find_element_by_name('确定').click()

    def test_user_manage_60(self):
        """删除用户 调试员无法删除调试员，可以删除值班管理员"""
        user = self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        # 添加调试员
        user_name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(
            random.randint(0, 100))
        self.sj.app_add_user(name=user_name, type='调试员', password='22223333', password_again='22223333', is_save=True)
        # 使用新增的调试员登录
        # self.sj.app_back_main_page()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_login(user_name=user_name, password='22223333')
        # 进入用户管理界面
        self.sj.app_menu('user')
        # 检查可以操作值班管理员、值班员
        self.assertTrue(self.sj.app_is_display('值班管理员'))
        self.assertTrue(self.sj.app_is_display('值班员'))
        # 检查无其他调试员（调试员无法删除其他调试员）
        self.sj.app_setting_user(user_num=2)
        self.assertFalse(self.sj.app_is_display('调试员'))
        # 使用系统管理员登录，删除该操作员
        self.sj.driver.find_element_by_id('user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=False, user_name=user_name)
        self.sj.app_edit_user('delete_btn')
        self.sj.driver.find_element_by_name('确定').click()

    @parameterized.expand(input=params_sup)
    def test_user_manage_61_0(self, name, user_num, password):
        """值班管理员设置值班员自动注销时间 -- 使用默认用户"""
        user = self.sj.app_login(user_num=user_num, password=password)
        self.sj.app_menu('user')
        # 修改值班员的自动注销时间
        self.sj.app_setting_user(user_num=2)
        self.sj.app_edit_user('time_spinner', time_tx=6)
        # 使用值班员登录
        self.sj.driver.find_element_by_id('user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_login(user_num=4, password='8888')
        # 用例上说明，误差时间不大于30秒
        sleep(60 * 6 + 15)
        # appium重新连接服务器(appium在1分钟无操作后自动退出)
        self.setUpClass()
        self.assertTrue(self.sj.app_is_display('登录'))

    @parameterized.expand(input=params_adj)
    def test_user_manage_61_1(self, name, user_num, password):
        """调试员设置值班管理员自动注销时间"""
        user = self.sj.app_login(user_num=user_num, password=password)
        self.sj.app_menu('user')
        self.sj.app_setting_user(is_add=True)
        user_name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(
            random.randint(0, 9))
        pwd = '123459'
        self.sj.app_add_user(name=user_name, type='值班管理员', password=pwd, password_again=pwd)
        # 修改自动注销时间
        self.sj.app_setting_user(user_name=user_name)
        self.sj.app_edit_user('time_spinner', time_tx=8)
        # 使用新增用户登录，验证自动注销时间
        self.sj.driver.find_element_by_id('user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        self.sj.app_login(user_name=user_name, password=pwd)
        # 用例上说明，误差时间不大于30秒
        sleep(60 * 8 + 15)
        # appium重新连接服务器(appium在1分钟无操作后自动退出)
        self.sj = Controller()
        try:
            self.assertTrue(self.sj.app_is_display('登录'))
        finally:
            # 使用调试员登录，删除新增用户
            self.sj.app_login(user_num=user_num, password=password)
            self.sj.app_menu('user')
            self.sj.app_setting_user(user_name=user_name)
            self.sj.app_edit_user('delete_btn')
            self.sj.driver.find_element_by_name('确定').click()


if __name__ == "__main__":
    # start_appium()
    # unittest.main(verbosity=2)
    run_suite(UserManage)