"""
    测试控制器登陆

"""
import sys
sys.path.append('..')
from libs import *
from parameterized import parameterized, param
import unittest


class Login(unittest.TestCase):

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
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    @parameterized.expand(input=params_all)
    def test_login_15(self, name, user_num, password):
        """各级用户正常登录系统"""
        # 登录
        user = self.sj.app_login(user_num=user_num, password=password)
        print(user)
        if user['type'] != '值班员':
            # 检查操作记录
            self.sj.app_menu('query')
            self.sj.app_query('operation')
            record = self.sj.app_query_history(record_num=1)
            record.pop(1)
            self.assertEqual(record, ['1', u'登录', user['name'], user['type']])
        else:
            self.assertFalse(self.sj.app_is_display('菜单'))
        try:
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_back_btn').click()
        except:
            pass

    @parameterized.expand(input=params_raw)
    def test_login_16(self, name, user_num, password):
        """以修改后的密码登录"""
        self.sj.app_login(user_num=user_num, password=password)
        new_password = password.replace('8888', '6666')
        self.sj.app_reset_password(new_password)
        self.assertTrue(self.sj.app_is_display('密码修改成功，请妥善保管新密码!'))
        # 回到主页
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_close').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
        # 使用新密码登录
        self.sj.app_login(user_num=user_num, password=new_password)
        self.assertTrue(self.sj.app_is_display('注销'))
        # 密码还原
        self.sj.app_reset_password(password)
        self.assertTrue(self.sj.app_is_display('密码修改成功，请妥善保管新密码!'))
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_close').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_edit_back_btn').click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_manage_back_btn').click()

    @parameterized.expand(input=params_all)
    def test_login_17_21(self, name, user_num, password):
        """分别用值班员、值班管理员、调试员、系统管理员登录系统后，按注销"""
        user = self.sj.app_login(user_num=user_num, password=password)
        # 点击取消，仍停留在取消界面
        self.sj.app_logout(is_sure=False)
        # 点击确定，正常退出登录
        self.sj.app_logout(is_sure=True)
        self.assertTrue(self.sj.app_is_display('登录'))
        # 注销后，检查手控盘开关是否关闭 ???待确定是否是checked元素
        value = self.sj.driver.find_element_by_name('手控盘').get_attribute('checked')
        self.assertTrue(value, 'false')
        self.sj.driver.quit()
        self.setUpClass()

    @parameterized.expand(input=params_sys_err)
    def test_login_err_22(self, name, user_num, password):
        """密码错误登录失败"""
        try:
            self.sj.driver.find_element_by_name('登录')
        except:
            self.sj.app_logout(is_sure=True)
        self.sj.app_login(user_num=user_num, password=password)
        self.assertTrue(self.sj.app_is_display('密码错误，请重新输入'))
        # 回到主界面
        self.sj.app_password('button_close2')
        self.sj.driver.quit()
        self.setUpClass()

    @parameterized.expand(input=params_sys_err)
    def test_login_err_23(self, name, user_num, password):
        """连续5次密码错误则退出登录窗口"""
        try:
            self.sj.driver.find_element_by_name('登录')
        except:
            self.sj.app_logout(is_sure=True)
        # 第1次错误登录
        self.sj.app_login(user_num=user_num, password=password)
        sleep(1)
        self.assertTrue(self.sj.app_is_display('密码错误，请重新输入'))
        # 第2次错误登录
        self.sj.app_login(password=err_password2, is_click_login=False)
        sleep(1)
        self.assertTrue(self.sj.app_is_display('密码错误，请重新输入'))
        # 第3次错误登录
        self.sj.app_login(password=err_password3, is_click_login=False)
        self.assertTrue(self.sj.app_is_display('密码错误，请重新输入'))
        # 第4次错误登录
        self.sj.app_login(password=err_password4, is_click_login=False)
        self.assertTrue(self.sj.app_is_display('密码错误，请重新输入'))
        # 第5次，错误登录，并回到主界面，提示"对不起，密码重试次数过多"
        self.sj.app_login(password=err_password5, is_click_login=False)
        self.sj.app_is_main_page()  # 回到主界面
        self.sj.driver.quit()
        self.setUpClass()

    @parameterized.expand(input=params_all)
    def test_login_err_24(self, name, user_num, password):
        """忘记密码"""
        # 点击登录用户到密码界面
        user = self.sj.app_login(user_num=user_num, password=None)
        sleep(1)
        # 点击忘记密码
        self.sj.app_password('text_forget_password')
        if user['type'] == '系统管理员' or user['type'] == '值班管理员':
            self.assertTrue(self.sj.app_is_display('请输入验证码'))
            # 检查下一步可点击
            value = self.sj.driver.find_element_by_name('下一步').get_attribute('clickable')
            self.assertEqual(value, 'true')
        elif user['type'] == '调试员':
            text = "请联系您的系统管理员修改密码，谢谢！"
            self.assertTrue(self.sj.app_is_display(text))
        elif user['type'] == '值班员':
            text = "请联系您的值班管理员修改密码，谢谢！"
            self.assertTrue(self.sj.app_is_display(text))
        self.sj.driver.quit()
        self.setUpClass()

    @parameterized.expand(input=params_all)
    def test_login_26(self, name, user_num, password):
        """观察各级用户的菜单权限"""
        user = self.sj.app_login(user_num=user_num, password=password)
        if user['type'] == '值班员':
            self.assertFalse(self.sj.app_is_display('菜单'))
        else:
            self.assertTrue(self.sj.app_is_display('菜单'))
        self.sj.driver.quit()
        self.setUpClass()

    @parameterized.expand(input=params_raw)
    def test_about_27(self, name, user_num, password):
        """关于功能测试"""
        user = self.sj.app_login(user_num=user_num, password=password)
        self.sj.app_menu('about')
        copyright = self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_copyright').get_attribute('text')
        company_location = self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_company_location').get_attribute('text')
        app_version = self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_app_version').get_attribute('text')
        telphone = self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_telephone').get_attribute('text')
        ele_sys_id = self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_system_id')
        system_id = ele_sys_id.get_attribute('text')
        self.assertEqual(copyright, '深圳市泛海三江电子股份有限公司 版权所有 2012-2032')
        self.assertEqual(company_location, '深圳市南山区南山大道光彩新天地公寓三层')
        self.assertEqual(app_version, 'V1.0')
        self.assertEqual(telphone, '(0755)86226969')
        self.assertEqual(system_id, 'CAD69B990')
        try:
            self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/about_back_btn').click()
        except:
            pass


if __name__ == "__main__":
    # sj = Controller()
    # user = sj.app_login(0)
    # # message = '%s %s 登录成功'% (user['type'], user['name'])
    # # print(sj.find_toast(message))
    # sj.driver.quit()
    # unittest.main(verbosity=2)
    run_suite(Login)