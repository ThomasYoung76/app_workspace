# coding: utf-8
"""
    控制器页面测试
"""
import sys
from time import sleep
from libs.log import *
import traceback
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class Controller(object):
    desired_caps = {
        'device': 'android',
        'platformName': 'Android',
        'platformVersion': '6.0.1',
        'deviceName': 'SABRESD-MX6DQ',
        'appPackage': 'com.fhsj.jbqbl.launcher',
        'appActivity': 'com.fhsj.jbqbl.launcher.ui.activities.NormalActivity'
    }

    def __init__(self):
        self.clog = sLog(log_name=os.path.basename(sys._getframe(1).f_code.co_filename)).log_write
        try:
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)
            self.driver.implicitly_wait(30)
            self.clog(get_current_info() + 'Starting App')
        except:
            self.clog(get_current_info() + 'Starting App fail. ', 'critical')
            sys.exit(-1)
        # # 点击欢迎页进入主界面
        # self.driver.find_element(By.ID, 'com.fhsj.jbqbl.launcher:id/normal_video').click()
        try:
            self.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/system_shield_back_btn").click()
        except:
            pass
        try:
            self.driver.find_element(By.ID, 'com.fhsj.jbqbl.launcher:id/normal_video').click()
        except:
            pass

    def app_login(self, user_num=None, user_name=None, password=None, is_click_login=True):
        """
        登录控制器，如果已有用户登录，则先注销后再登录
        界面：登录
        :param user_num: int 登录用户的序号，如user_num为1，表示登录第一个用户
        :param user_name: str 登录的用户名，与user_num不能同时赋值。
        :param password: str 密码
        :return:
                登录成功返回{'name': login_username, 'type': login_usertype, 'time': login_time} 用户名，用户类型，
                登录失败返回：{'name': login_username, 'type': login_usertype}
        """
        # 登录用户的序号和登录的用户名不能同时存在，否则退出登录，抛出异常
        try:
            assert (not user_num) or (not user_name)
        except:
            self.clog(get_current_info() + 'Login fail. Param user_num and param user_name cannot be all exist', 'Error')
            raise AssertionError('Params user_num and user_name cannot coexist. Please choose one of them to login')

        login_username = None
        login_usertype = None
        if is_click_login:
            try:
                # 获取登录按钮
                ele_login = self.driver.find_element(By.ID, 'com.fhsj.jbqbl.launcher:id/login_bar_login_btn')
            except NoSuchElementException:
                # 优化 -> 判断待登录用户是否已登录,若已登录则不再重复登录
                raw_user_name = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/login_bar_user_name').get_attribute('text')
                raw_user_type = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/login_bar_user_type').get_attribute('text')
                if raw_user_name == user_name:
                    self.clog(get_current_info() + 'User is already logined. user: %s' % raw_user_name)
                    return {'name': raw_user_name, 'type': raw_user_type}
                elif raw_user_type == '系统管理员' and user_num == 1:
                    self.clog(get_current_info() + 'User is already logined. user: %s' % raw_user_name)
                    return {'name': raw_user_name, 'type': raw_user_type}
                else:
                    # 注销后再登录
                    self.app_logout()
                    ele_login = self.driver.find_element(By.ID, 'com.fhsj.jbqbl.launcher:id/login_bar_login_btn')
            ele_login.click()
            self.clog(get_current_info() + 'Click login')
        if user_num:
            user_index = user_num - 1
            ele_users = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userName')
            ele_types = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userType')
            # 获取登录用户名和用户类型
            login_username = ele_users[user_index].get_attribute('text')
            login_usertype = ele_types[user_index].get_attribute('text')
            ele_users[user_index].click()
            if not password:
                return {'name': login_username, 'type': login_usertype}
        if user_name:
            login_username = user_name
            ele_users = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userName')
            ele_types = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userType')
            for i in range(len(ele_users)):
                if ele_users[i].get_attribute('text') == user_name:
                    login_usertype = ele_types[i].get_attribute('text')
                    break
                else:
                    login_usertype = None
            self.driver.find_element_by_name(user_name).click()
            if not password:
                return {'name': login_username, 'type': login_usertype}
        if password:
            for i in range(len(password)):
                self.driver.find_element(By.ID, 'com.fhsj.jbqbl.launcher:id/button' + password[i]).click()
        return {'name': login_username, 'type': login_usertype}
        # try:
        #     # 获取登录时间
        #     login_time = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/top_bar_current_time_text').get_attribute('text')
        #     login_time = login_time[:-3]    # 去掉秒，只精确到分
        #     self.c_log(get_current_info() + 'Login app success. login time: %s. username: %s. usertype: %s. password: %s' %(login_time, login_username, login_usertype, password))
        #     return {'name': login_username, 'type': login_usertype, 'time': login_time}
        # except NoSuchElementException:
        #     self.c_log(get_current_info() + 'Login app fail. user_num: %s. password: %s' % (user_num, password), 'warning')
        #     return None
        # except:
        #     self.c_log(get_current_info() + 'cannot get current time', 'warning')
        #     return None

    def app_logout(self, is_sure=True):
        """
        注销
        :param is_sure: 是否确定推出登录
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/login_bar_logout_btn').click()
        if is_sure:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_logout_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_logout_cancel').click()
        self.clog(get_current_info() + 'Logout current user. is_sure: %s' % is_sure)

    def app_user(self, btn_id):
        """
        选择用户界面。元素：关闭、用户名、用户类型
        :param btn_id: 按钮id。如：button_close1、text_userName、text_userType
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % btn_id).click()
        self.clog(get_current_info() + 'Click %s in User Surface' % btn_id)

    def app_password(self, btn_id):
        """
        输入密码界面。元素：关闭、数字按钮、回退、删除、密码进度显示、忘记密码、
        :param btn_id: 按钮id。如：button_close2、button0-9、button_backspace、button_delete、image_dot8_1-8、text_forget_password
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s'% btn_id).click()
        self.clog(get_current_info() + 'Click %s in Password Surface' % btn_id)

    def app_forget_password(self, btn_id):
        """
        忘记密码界面。元素：管理员关闭、非管理员关闭、下一步、验证码、序列号、二维码
        :param btn_id: button_close3、button_close4、text_next、edit_code、text_serial_number、image_qrcode
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % btn_id).click()
        self.clog(get_current_info() + 'Click %s in Password Reset Surface' % btn_id)

    def app_reset_password_surface(self, btn_id):
        """
        修改密码界面。元素：数字按钮、回退、删除
        :param btn_id: 按键id。如：button0-9、button_backspace、button_delete
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s_change_layout'% btn_id).click()

    def app_input_password(self, password):
        """输入密码"""
        for i in str(password):
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/button%s_change_layout' % i).click()
        self.clog(get_current_info() + 'Input password. password: %s' % password)

    def app_reset_password(self, new_password, user_num=1):
        """
        修改用户密码
        :param new_password: str新密码
        :param user_num: 用户序号，默认为1，修改当前用户
        :return:
        """
        # 进入用户管理界面
        self.app_menu('user')
        # user_num为1，默认均修改当前登录用户
        self.app_setting_user(user_num=user_num)
        self.app_edit_user('change_password_btn')
        # 修改密码
        for i in new_password:
            self.app_reset_password_surface('button%s' % i)
        self.clog(get_current_info() + 'Input new password. password: %s' % new_password)
        # 再次输入密码
        for i in new_password:
            self.app_reset_password_surface('button%s' % i)
        self.clog(get_current_info() + 'Input new password again. password: %s' % new_password)

    # 废弃 -- 好处：可以增加日志，坏处：IDE无法联想该元素的对象方法
    def find_element(self, by, value):
        """
        查找单个元素
        :param by: 方式，如id，name, class name等等
        :param value: 对应方式的值，如id值，name值等等
        :return: 元素对象
        """
        if by.lower() == By.ID:
            element = self.driver.find_element_by_id(value)
        elif by.lower() == By.NAME:
            element = self.driver.find_element_by_name(value)
        elif by.lower() == By.CLASS_NAME:
            element = self.driver.find_element_by_class_name(value)
        elif by.lower() == By.TAG_NAME:
            element = self.driver.find_element_by_tag_name(value)
        else:
            element = None
        self.driver.implicitly_wait(20)
        if isinstance(element, object):
            self.clog(get_current_info() + 'Find element by %s success. %s is: %s.' % (by, by, value))
        else:
            self.clog(get_current_info() + 'Find element by %s fail. %s is: %s.' % (by, by, value))
        return element

    # 废弃 -- 好处：可以增加日志，坏处：IDE无法联想该元素的对象方法
    def find_elements(self, by, value):
        """
        查找多个元素
        :param by: 方式，如id，name, class name等等
        :param value: 对应方式的值，如id值，name值等等
        :return: 多个元素对象组成的列表
        """
        if by.lower() == By.ID:
            elements = self.driver.find_elements_by_id(value)
        elif by.lower() == By.NAME:
            elements = self.driver.find_elements_by_name(value)
        elif by.lower() == By.CLASS_NAME:
            elements = self.driver.find_elements_by_class_name(value)
        elif by.lower() == By.TAG_NAME:
            elements = self.driver.find_elements_by_tag_name(value)
        else:
            elements = None
        self.driver.implicitly_wait(20)
        if isinstance(elements, list):
            self.clog(get_current_info() + 'Find elements by %s success. %s is: %s.' % (by, by, value))
        else:
            self.clog(get_current_info() + 'Find elements by %s fail. %s is: %s.' % (by, by, value))
        return elements

    def find_toast(self,message):  
        """判断toast信息"""
        try:
            WebDriverWait(self.driver,30, poll_frequency=0.1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,message)))
            self.clog(get_current_info() + 'Toast message exist. message is: %s.' % message)
            return True
        except:
            print(traceback.print_exc())
            self.clog(get_current_info() + 'Toast message not exist. message is: %s.' % message, 'warning')
            return False

    def app_main_page(self, text=None, ele_id=None):
        """
        主页界面
        :param text: 控件文本name 点击
        :param ele_id: 点击控件id，如：fire（火警）、linkage(联动)、fault（故障）
        :return:
        """
        if text:
            self.driver.find_element_by_name(text).click()
            self.clog(get_current_info() + 'Operate in main page. click text %s' % text)
        if ele_id:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/notices_%s_notice_btn'% ele_id).click()
            self.clog(get_current_info() + 'Operate in main page. click element id: %s' % ele_id)

    def app_main_page_get_notice(self, get_notice_info=False, count_info=False):
        """
        获取报警信息
        :param get_notice_info: list(list(), list())获取报警信息，返回最后一页所有报警内容[(id, location, device_name, time, company_code),(...), ...]
        :param count_info: list(str) 统计各类报警总数 [count_fire, count_linkage, count_fault]
        :return:
        """
        if count_info:
            ele_notice_fire = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/notices_fire_notice_btn')
            # 火警数
            count_fire = ele_notice_fire.get_attribute('text')[-3:]
            ele_notice_linkage = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/notices_linkage_notice_btn')
            # 联动故障数
            count_linkage = ele_notice_linkage.get_attribute('text')[-3:]
            ele_notice_fault = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/notices_fault_notice_btn')
            # 故障数
            count_fault = ele_notice_fault.get_attribute('text')[-3:]
            return [count_fire, count_linkage, count_fault]
        if get_notice_info:
            # 滑到最后一页(140, 1000)-> (140, 310)
            for i in range(10):
                self.driver.swipe(start_x=140, start_y=1000, end_x=140, end_y=310, duration=500)
            ele_notice_item = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_item')
            ele_notice_id = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_id')
            ele_notice_location = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_location')
            ele_notice_device_name = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_device_name')
            ele_notice_time = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_time')
            ele_notice_company_code = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_notice_company_code')
            list_notice = list()
            # id行没显示时,去掉其他多余显示的控件
            if len(ele_notice_id) < len(ele_notice_device_name):
                ele_notice_item.pop(0)
                ele_notice_device_name.pop(0)
                ele_notice_time.pop(0)
                ele_notice_company_code.pop(0)
            for i in range(len(ele_notice_item)):
                list_notice_single = list()
                try:
                    notice_id = ele_notice_id[i].get_attribute('text')
                    notice_location = ele_notice_location[i].get_attribute('text')
                    notice_device_name = ele_notice_device_name[i].get_attribute('text')
                    notice_time = ele_notice_time[i].get_attribute('text')
                    notice_company_code = ele_notice_company_code[i].get_attribute('text')
                except IndexError:
                    continue        # 该条报警显示不完全，跳过处理
                list_notice_single.append(notice_id)
                list_notice_single.append(notice_location)
                list_notice_single.append(notice_device_name)
                list_notice_single.append(notice_time)
                list_notice_single.append(notice_company_code)
                list_notice.append(list_notice_single)
            self.clog(get_current_info() + 'Get notice info')
            return list_notice

    def app_menu(self, menu_id='', is_click_menu=True, is_click_back=False):
        """
        默认在主界面点击菜单按钮进入菜单栏，如本机设置、系统管理、联动设置、调试管理、关于、向导、返回、区栋层
        :param is_click_menu: 是否在主界面点击菜单按钮
        :param menu_id: guide, about, time, user, query, statistics, debug, storage_manage, device_type_manage, shield，location
        :return:
        """
        if is_click_menu:
            # 点击菜单栏进入菜单界面
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/login_bar_menu_btn').click()
            self.clog(get_current_info() + 'Enter menu surface')
        # 从菜单主界面进入相应界面，如关于、向导、用户、时间、记录查询、系统管理、联动设置、调试管理、区栋层返回
        if menu_id:
            whole_id = 'com.fhsj.jbqbl.launcher:id/menu_%s_btn' % menu_id
            self.driver.find_element_by_id(whole_id).click()
            self.clog(get_current_info() + 'Enter %s surface' % menu_id)
        if is_click_back:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/menu_back_btn').click()
            self.clog(get_current_info() + 'Click back in menu')


    def app_query(self, history_id):
        """
        进入各类型历史记录。如：火警记录、联动记录、故障记录、操作记录、返回
        :param history_id: 历史记录id，如：fire、linkage、fault、operation
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_btn' % history_id).click()
        self.clog(get_current_info() + 'Enter %s surface' % history_id)

    def app_query_history(self, record_id=None, record_num=1, record_type='operation'):
        """
        操作记录界面。
        功能1：点击按钮，如：打印、清除、按时间排序、筛选；
        功能2：获取记录表内容,如：[序号、时间、操作、用户、用户类型]
        :param record_id: 值不为空，点击id:print、delete、order、filter，若值为空则获取记录表内容
        :param record_num： 获取第record_num条记录，值为0则获取当页所有记录。默认获取第一条记录
        :param record_type: 记录类型，共4中：'fire', 'linkage', 'fault', 'operation'
        :return: 如果操作id不为None，则点击，返回None，反之：获取历史记录表的内容，返回列表
        """
        if record_id:
            whole_id = 'com.fhsj.jbqbl.launcher:id/system_history_%s_%s_btn' % (record_type, record_id)
            self.driver.find_element_by_id(whole_id).click()
            return None
        else:
            # 获取所有记录表内容项
            items = self.driver.find_elements_by_id('system_history_%s_item' % record_type)
            list_items = []
            if record_type == 'operation':
                for i in range(len(items)):
                    list_item = []
                    opr_num = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_operation_num').get_attribute('text')
                    opr_time = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_operation_time').get_attribute('text')
                    opr_opr = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_operation_operation').get_attribute('text')
                    opr_user = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_operation_user').get_attribute('text')
                    ope_user_type = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_operation_user_type').get_attribute('text')
                    list_item.append(opr_num)
                    list_item.append(opr_time)
                    list_item.append(opr_opr)
                    list_item.append(opr_user)
                    list_item.append(ope_user_type)
                    list_items.append(list_item)
            else:
                for i in range(len(items)):
                    list_item = []
                    num = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_num' % record_type).get_attribute('text')
                    if num:
                        time = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_time' % record_type).get_attribute('text')
                        device_type = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_device_type' % record_type).get_attribute('text')
                        location = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_location' % record_type).get_attribute('text')
                        event = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_event' % record_type).get_attribute('text')
                        debug_code = items[i].find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_%s_debug_code' % record_type).get_attribute('text')
                        list_item.append(num)
                        list_item.append(time)
                        list_item.append(device_type)
                        list_item.append(location)
                        list_item.append(event)
                        list_item.append(debug_code)
                        list_items.append(list_item)
            if record_num:
                # 返回第record_num条记录
                return list_items[record_num-1]
            else:
                # 如果record_num为0或者None则返回当页所有记录
                return list_items

    def app_setting_user(self, user_num=None, user_name=None, is_add=False):
        """
        在用户管理界面进行操作，添加用户或者编辑用户。元素有：添加新用户、用户名、用户类型
        :param user_num: int 用户序号，如第一位为1
        :param user_name: str 用户名，通过用户名选择用户进行编辑, 与user_name不能同时赋值
        :param is_add: 是否添加新用户，若添加新用户，则其他参数无效
        :return: None
        """
        if not is_add:
            # 用户序号和用户名不能同时存在，否则抛出异常
            try:
                assert (not user_num) or (not user_name)
            except:
                self.clog(
                    get_current_info() + 'Setting user fail. Param user_num and param user_name cannot be all exist',
                    'Error')
                raise AssertionError(
                    'Params user_num and user_name cannot coexist. Please choose one of them to set')
            if user_num:
                ele_users = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/text_userName')
                user_num = user_num - 1
                ele_users[user_num].click()
                self.clog(get_current_info() + 'Enter Edit User Surface in User Manage Surface by user_num. user_num: %s' % user_num)
            if user_name:
               self.driver.find_element_by_name(user_name).click()
               self.clog(get_current_info() + 'Enter Edit User Surface in User Manage Surface by user name. user name: %s' % user_name)
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/add_user').click()
            self.clog(get_current_info() + 'Enter Add User Surface in User Manage')

    def app_edit_user(self, edit_id, time_tx=None):
        """
        用户管理中的用户编辑界面。元素有：修改密码、删除、自动注销时间
        :param edit_id: 编辑项的id，如：change_password_btn、delete_btn、time_spinner
        :param time_tx: 自动注销时间，当edit_id为time_spinner时，设置该值生效
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_edit_%s' % edit_id).click()
        self.clog(get_current_info() + 'Edit User. Edit type: %s' % edit_id)
        if edit_id == 'time_spinner' and time_tx:
            if int(time_tx) <= 11:
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 17:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 23:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 29:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(23)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            else:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(23)).click()
                self.driver.find_element_by_name(str(29)).click()
                self.driver.find_element_by_name(str(30)).click()
            self.clog(get_current_info() + 'Edit user set time_spinner. time_spinner: %s' % time_tx)

    def app_is_display(self, text):
        """
        判断文本是否出现
        :param text: 控件的name
        :return:
        """
        try:
            self.driver.find_element_by_name(text).is_displayed()
            self.clog(get_current_info() + 'Text is displayed. text: %s' % text)
            return True
        except:
            self.clog(get_current_info() + 'Text is not displayed. text: %s' % text, 'warning')
            return False

    def app_is_checked(self, ele_id):
        """
        判断CheckBox控建是否被勾选
        :param ele_id: CheckBox控件的id
        :return: bool
        """
        ele = self.driver.find_element_by_id(ele_id)
        if ele.get_attribute('checked') == 'true':
            return True
        else:
            return False

    def app_is_main_page(self):
        """
        判断app当前是否处于主页
        :return: bool
        """
        flag = False  # 主页标志
        try:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/main_show_layout').is_displayed()
            self.clog(get_current_info() + 'app is in main page now.')
            flag = True
        except:
            self.clog(get_current_info() + 'app is not in main page now.', 'warning')
        return flag

    def app_get_current_time(self):
        """获取当前系统时间"""
        cur_time = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/top_bar_current_time_text').get_attribute('text')
        self.clog(get_current_info() + 'Current time is: %s' % cur_time)
        return cur_time

    def app_back_main_page(self):
        """从任意界面回到主机"""
        flag = self.app_is_main_page()
        # 如果没有回到主页，试图点击关闭按钮，或者返回按钮操作
        # 关闭密码界面
        if not flag:
            try:
                self.app_password('button_close2')
                flag = self.app_is_main_page()
            except:
                pass
        # 关闭用户界面
        if not flag:
            try:
                self.app_user('button_close1')
                flag = self.app_is_main_page()
            except:
                pass
        # 关闭重置密码界面
        if not flag:
            try:
                self.app_password('button_close3')
                flag = self.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.app_password('button_close4')
                flag = self.app_is_main_page()
            except:
                pass
        # 从菜单返回到首页
        if not flag:
            try:
                self.app_menu(is_click_menu=False, is_click_back=True)
                flag = self.app_is_main_page()
            except:
                pass
        return flag

    def app_get_size(self):
        """获取屏幕大小"""
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x,y)

    def app_add_user(self, name=None, type='值班员', password=None, password_again=None, time_tx=None, is_save=True):
        """
        添加用户
        :param name: 用户名
        :param type: 用户类型，'调试员','值班管理员','值班员'
        :param password: str密码
        :param password_again: str确认密码
        :param time_tx: 自动注销时间
        :param is_save: 是否保存
        :return: bool 添加成功，返回True，添加失败，返回False
        """
        if name:
            ele_name = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_user_name')
            ele_name.click()
            ele_name.send_keys(name)
            # 隐藏键盘
            self.driver.hide_keyboard()
            # ele_name.send_keys(Keys.ENTER)
        if type:
            self.driver.find_element_by_name(type).click()
        if password:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_change_password_btn').click()
            # 设置密码
            for i in str(password):
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/button%s_change_layout'% i).click()
        # 再次输入密码
        if password_again:
            for i in str(password_again):
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/button%s_change_layout'% i).click()
        # 选择自动注销时长
        if time_tx:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_time_spinner').click()
            if int(time_tx) <= 11:
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 17:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 23:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            elif int(time_tx) <= 29:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(23)).click()
                self.driver.find_element_by_name(str(time_tx)).click()
            else:
                self.driver.find_element_by_name(str(11)).click()
                self.driver.find_element_by_name(str(17)).click()
                self.driver.find_element_by_name(str(23)).click()
                self.driver.find_element_by_name(str(29)).click()
                self.driver.find_element_by_name(str(30)).click()
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/user_add_save_btn').click()
        self.clog(get_current_info() + 'Add user with args. name: %s, type: %s. password: %s. password_again: %s. time_spinning: %s. is_save: %s' %
                  (name, type, password, password_again, time_tx, is_save))
        try:
            self.driver.find_element_by_name('用户').is_displayed()
            self.clog(get_current_info() + 'Add user success. user name: %s. user type: %s' % (name, type))
            return True
        except NoSuchElementException:
            self.clog(get_current_info() + 'Add user fail.', 'warning')
            return False

    def app_local_device(self, dev_id):
        """
        在设备管理界面点击设备。设备元素：显示器、485手控盘、广播控制盘、打印机、电源、保存
        :param dev_id: 设备元素id，对应如：screen_btn、handler、broadcast、printer、power、save
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/local_device_%s_btn' % dev_id).click()
        self.clog(get_current_info() + 'Choose %s in Device Manage Surface' % dev_id)

    def app_local_device_handler(self, is_batch_register=False, is_auto_register=False, register_num=None):
        """
        设备管理界面中设置485手控盘, 自动注册、批量注册、选中手控盘序号进行注册
        :param is_batch_register: bool 是否批量注册
        :param is_auto_register: bool 是否自动注册
        :param register_num: int 单个注册时的注册序号，点击该
        :return:
        """
        # 3个参数中只有1个值可以为True
        try:
            assert (not is_batch_register) or(not is_auto_register)
            assert (not is_batch_register) or (not register_num)
            assert (not is_auto_register) or (not register_num)
        except AssertionError as msg:
            self.clog(get_current_info() + 'Only one of the args can be True')
            raise AssertionError(msg)
        if is_batch_register:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/local_device_handler_batches_operation_btn').click()
        elif is_auto_register:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/local_device_handler_auto_register_btn').click()
        elif register_num:
            # 选中手控盘序号进行注册
            checkboxes = self.driver.find_elements_by_class_name('android.widget.CheckBox')
            register_num = register_num -1
            checkboxes[register_num].click()
        self.clog(get_current_info() + 'Register 486手控盘. is batch register: %s. is auto register: %s. register_num: %s' % (str(is_batch_register), str(is_auto_register), register_num))

    def app_handler_batch_register(self, is_register=True, is_submit=True):
        """
        485手控盘批量注册界面，元素： 确定、取消、注册
        分辨率：{u'width': 1920, u'height': 1079}
        坐标：从="[548,483][570,529]"  号="[783,483][805,529]"  到="[908, 483][930, 529]"  号="[1148,483][1170,529]"
        推算出32号的坐标：(1050, 463)
        :is_register: 是否注册
        :is_submit: 是否确定
        :return:
        """
        # 注册框
        ele_check = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_checkbox')
        is_checked = ele_check.get_attribute('checked')
        # 注册则勾选该框，否则取消勾选该框
        if is_register:
            if is_checked == 'false':
                ele_check.click()
        else:
            if is_checked:
                ele_check.click()
        if is_submit:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_cancel').click()
        self.clog(get_current_info() + 'Batch register 485手控盘 with args. is register: %s. is submit: %s' % (is_register, is_submit))

    def app_local_device_broadcast(self, num, point, is_register=True, is_save=True):
        """
        广播控制盘界面注册/去注册序号为num的广播控制盘

        分辨率：{u'width': 1920, u'height': 1079}
        坐标信息：表格每行高度60，每行之间的线条高度为2，每个表格总共8行，高度范围为（342，863），
        从最下一行中间滑到最上一行中间y轴的变化为（863-60/2=833，833+62*7）=（833，399）
        x轴始终不变，取值为795 +(984-795)/2 = 890

        :param num: int 待注册的广播控制盘的序号,范围0-30
        :param point: int 广播控制盘的点数
        :param is_register: 是否注册，为False表示取消注册
        :return:
        """
        # 注册框集
        ele_regist = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_register')
        for i in range(5):
            # 序号元素集
            order_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_name')
            # 表格中最小序号和最大序号
            min_num = int(order_num[0].get_attribute('text'))
            max_num = int(order_num[-1].get_attribute('text'))
            if num >= min_num and num <= max_num:
                index = num - min_num
                is_check = ele_regist[index].get_attribute('checked')
                if is_register:
                    # 未注册则勾选注册
                    if is_check == 'false':
                        ele_regist[index].click()
                else:
                    # 已注册则取消注册
                    if is_check == 'true':
                        ele_regist[index].click()
                break
            else:
                # 从最后一行中间上滑到第一行中间
                self.driver.swipe(890, 833, 890, 399, 2000)
        if is_register:
            # 获取新注册的广播盘在当页所有已注册广播盘中的索引位置
            count = 0   # 已注册的数量
            for i in range(len(ele_regist)):
                # 判断是否已注册
                is_checked = ele_regist[i].get_attribute('checked')
                if is_checked == 'true':
                    # 是否是新注册的，若索引值为新注册是设备的索引值， 则获取新注册的广播盘在所有已注册的广播盘中的索引位置，用于选择点数
                    if i == index:
                        num_register = count    # 获取新注册广播盘的索引值
                        break
                    count += 1
            ele_point = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_point_%s'% str(point))
            try:
                ele_point[num_register].click()
            except IndexError as msg:
                self.clog(get_current_info() + 'did not get index of new broadcase device', 'Error')
                raise IndexError(msg)
        if is_save:
            self.app_local_device('save')
        self.clog(get_current_info() + "Register device broadcast. num: %s. point: %s. is_register: %s. is_save: %s" % (num, point, is_register, is_save))

    def app_local_device_broadcast_check_point(self, num, point):
        """
        检查num号broadcast的point点已被选中
        :param num: broadcast的序号
        :param point: 点数，值为30，60，90
        :return:
        """
        # 注册框集
        ele_regist = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_register')
        # 切换到broadcast num的位置，并判断已被注册
        for i in range(5):
            # 序号元素集
            order_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_name')
            # 表格中最小序号和最大序号
            min_num = int(order_num[0].get_attribute('text'))
            max_num = int(order_num[-1].get_attribute('text'))
            if num >= min_num and num <= max_num:
                index = num - min_num
                is_check = ele_regist[index].get_attribute('checked')
                # 未注册则检查失败
                if is_check == 'false':
                    self.clog(get_current_info() + 'Check broadcast error. broadcast num %s is not registed.' % num, 'Error')
                    return False
            else:
                # 从最后一行中间上滑到第一行中间
                self.driver.swipe(890, 833, 890, 399, 2000)
        # 获取新注册的广播盘在当页所有已注册广播盘中的索引位置
        count = 0  # 已注册的数量
        for i in range(len(ele_regist)):
            # 判断是否已注册
            is_checked = ele_regist[i].get_attribute('checked')
            if is_checked == 'true':
                # 是否是新注册的，若索引值为新注册是设备的索引值， 则获取新注册的广播盘在所有已注册的广播盘中的索引位置，用于选择点数
                if i == index:
                    num_register = count  # 获取新注册广播盘的索引值
                    break
                count += 1
        # 检查点数是否被选中
        ele_point = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/broadcast_control_panel_point_%s_icon' % str(point))
        try:
            check_point = ele_point[num_register].get_attribute('selected')
            if check_point == 'true':
                self.clog(get_current_info() + 'Check success. broadcast num %s point %s has been selected' % (num , point))
                return True
            else:
                self.clog(
                    get_current_info() + 'Check fail. broadcast num %s point %s did not be selected' % (num, point), 'warning')
                return False
        except IndexError as msg:
            self.clog(get_current_info() + 'did not get index of new broadcase device', 'Error')
            raise IndexError(msg)

    def app_linkage_programme(self, linkage_pro_id):
        """
        联动编程界面。点击框有：统计、筛选、添加、全部生效、全部失效、全部删除
        :param linkage_pro_id: 控件id，分别为：statistics、filter、add、effective、dis_effective、delete
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_programme_%s_btn'%linkage_pro_id).click()
        self.clog(get_current_info() + 'Operate in linkage programme. operation: %s' % linkage_pro_id)

    def app_linkage_add(self, linkage_text):
        """
        添加联动。控件有：联动原则、系统联动。。。
        :param linkage_text: 控件文本
        :return:
        """
        self.driver.find_element_by_name(linkage_text).click()
        self.clog(get_current_info() + 'Add linkage. text: %s' % linkage_text)

    def app_linkage_add_broadcast(self, is_input=False, is_out=False, is_save=False, is_save_continue=False):
        """
        联动编程->添加->广播控制点设置
        :param is_input: 编辑输入条件
        :param is_out: 编辑输出结果
        :param is_save: 保存
        :param is_save_continue: 保存并继续添加
        :return:
        """
        if is_input:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_broadcast_input_click_view').click()
        if is_out:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_broadcast_edit_output').click()
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_broadcast_save_btn').click()
        if is_save_continue:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_broadcast_save_continue_add_btn').click()

    def app_linkage_add_broadcast_input(self, input_panel=None, input_point=None, is_submit=False):
        """
        联动编程->添加->广播控制点设置->选择输入条件
        :param input_panel: 广播控制盘
        :param input_point: 控制点
        :param is_submit: 是否确定
        :return:
        """
        if input_panel:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_broadcast_input_panel_spinner').click()
            self.driver.find_element_by_name(input_panel).click()
        if input_point:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_broadcast_input_point_spinner').click()
            sleep(2)
            # self.driver.find_element_by_name(input_point).click()
            self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[int(input_point)-1].click()
        if is_submit:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_broadcast_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_broadcast_cancel').click()

    def app_location(self, comm_num=None, comm_locate=None, build_num=None, build_locate=None, floor_num=None, is_save=False, is_register=(True, True, True)):
        """
        联动设置-区栋层注册/去注册。控件有：批量操作、区号、区注册、区位置、区扩展、栋号、栋注册、栋位置、栋扩展、层号、层注册(暂不支持滑动页面)
        参数要求：comm_locate赋值时，必须先给comm_num赋值，先有区号后有栋号最后有层号
        :param is_batch: bool 是否批量操作
        :param comm_num: int 区号
        :param comm_locate: str 区位置（区号存在，才能编辑区位置）
        :param build_num: int 栋号
        :param build_locate: str 栋位置（栋号存在，才能编辑栋位置）
        :param floor_num: int 层号
        :param is_save: bool 是否保存
        :param is_register: bool_tuple （True, True, True）3个bool值分别代表是否注册区、栋、层。默认值为（True, True, True）表示全部注册
        :return: 区栋层的状态信息，如区扩展（comm_icon）、栋扩展（build_icon）是否可被选中，区号（is_comm_reg）是否被注册, 栋号（is_build_reg）是否被注册
        层号（is_floor_reg)是否被注册， 区位置信息（comm_loc），栋位置信息（build_loc）
        result = {   'comm_icon': bool,
            'is_comm_reg': bool,
            'build_icon': bool,
            'is_build_reg': bool,
            'is_floor_reg': bool,
            'comm_loc': str,
            'build_loc': str}
        """
        # 参数值断言
        if comm_locate:
            assert comm_num         # 区位置赋值时，必须赋值区号
        if build_locate:
            assert build_num        # 栋位置赋值时，必须赋值栋号
        result = {}
        func = lambda x: True if x == 'true' else False # 判断属性值是否为‘true'
        if comm_num:
            # 区选择框
            ele_check_comm = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_register')
            # 区号控件集
            ele_comm_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_num')
            list_comm_num = [ele_comm_num[i].get_attribute('text') for i in range(len(ele_comm_num))]   # 区号列表
            comm_index = list_comm_num.index(str(comm_num))  # 通过区号获取区号所在控件的索引值
            is_checked = ele_check_comm[comm_index].get_attribute('checked')
            # 注册/去注册
            if is_register[0]:
                if is_checked == 'false':
                    ele_check_comm[comm_index].click()
            else:
                if is_checked == 'true':
                    ele_check_comm[comm_index].click()
            # 重新获取区号的注册信息
            ele_check_comm = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_register')
            is_comm_checked = ele_check_comm[comm_index].get_attribute('checked')
            is_comm_register = func(is_comm_checked)     # 区号是否被注册
            result['is_comm_reg'] = is_comm_register
            # 区位置信息
            if comm_locate:
                ele_check_comm_loc = self.driver.find_elements_by_id(
                    'com.fhsj.jbqbl.launcher:id/location_community_list_desc')
                ele_check_comm_loc[comm_index].click()
                ele_input = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_description_edit')
                ele_input.click()  # 点击输入框呼出键盘
                ele_input.clear()
                ele_input.send_keys(comm_locate)
                self.driver.hide_keyboard()  # 隐藏键盘
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_description_confirm').click()
                # 获取区位置信息
                ele_check_comm_loc = self.driver.find_elements_by_id(
                    'com.fhsj.jbqbl.launcher:id/location_community_list_desc')
                comm_loc = ele_check_comm_loc[comm_index].get_attribute('text')
                result['comm_loc'] = comm_loc
            # 区扩展图标,注册则展开，去注册则隐藏（通过is_selected的值判断是否被展开）
            ele_check_comm_icon = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_expand_icon')
            is_selected_raw = ele_check_comm_icon[comm_index].get_attribute('selected')
            if is_register[0]:
                if is_selected_raw != 'true':
                    ele_check_comm_icon[comm_index].click()
            else:
                if is_selected_raw == 'true':
                    ele_check_comm_icon[comm_index].click()
            # 重新获取区扩展图标的状态信息
            ele_check_comm_icon = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_expand_icon')
            is_selected = ele_check_comm_icon[comm_index].get_attribute('selected')
            result['comm_icon'] = func(is_selected)     # 区号扩展图标是否可被选中
        if build_num:
            # 栋选择框
            ele_check_build= self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_register')
            if len(ele_check_build) == 0:
                if is_save:
                    self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_list_save_btn').click()
                self.clog(get_current_info() + 'Building info has been hidden, May be community has not been registed. comm_num: %s' % comm_num, 'warning')
                return result
            # 栋号控件集
            ele_build_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_num')
            list_build_num = [ele_build_num[i].get_attribute('text') for i in range(len(ele_build_num))]    # 栋号列表
            build_index = list_build_num.index(str(build_num))   # 栋号索引
            is_checked = ele_check_build[build_index].get_attribute('checked')
            # 注册/去注册
            if is_register[1]:
                if is_checked == 'false':
                    ele_check_build[build_index].click()
            else:
                if is_checked == 'true':
                    ele_check_build[build_index].click()
            # 重新获取栋号的注册信息
            ele_check_build = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_register')
            is_build_checked = ele_check_build[build_index].get_attribute('checked')
            is_build_register = func(is_build_checked)  # 栋号是否被注册
            result['is_build_reg'] = is_build_register
            # 栋位置信息
            if build_locate:
                ele_check_build_loc = self.driver.find_elements_by_id(
                    'com.fhsj.jbqbl.launcher:id/location_building_list_desc')
                ele_check_build_loc[build_index].click()
                ele_input = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_description_edit')
                ele_input.click()  # 点击输入框呼出键盘
                ele_input.clear()
                ele_input.send_keys(build_locate)
                self.driver.hide_keyboard()  # 隐藏键盘
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_description_confirm').click()
                # 获取栋位置信息
                ele_check_build_loc = self.driver.find_elements_by_id(
                    'com.fhsj.jbqbl.launcher:id/location_building_list_desc')
                build_loc = ele_check_build_loc[build_index].get_attribute('text')
                result['build_loc'] = build_loc
            # 栋扩展图标
            ele_check_build_icon = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_expand_icon')
            ele_check_build_icon.pop(0)     # 列表中第一个控件应该是不存在的较为合理，这里先规避处理
            is_selected_raw = ele_check_build_icon[build_index].get_attribute('selected')
            if is_register[1]:
                if is_selected_raw != 'true':
                    ele_check_build_icon[build_index].click()
            else:
                if is_selected_raw == 'true':
                    ele_check_build_icon[build_index].click()
            ele_check_build_icon = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_expand_icon')
            ele_check_build_icon.pop(0)  # 列表中第一个控件应该是不存在的较为合理，这里先规避处理
            is_selected = ele_check_build_icon[build_index].get_attribute('selected')
            # 点击后是否被选中来判断该图标是否可被点击
            result['build_icon'] = func(is_selected)    # 栋号扩展图标是否可被选中
        if floor_num:
            # 层选择框
            ele_check_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_floor_list_register')
            # 层号
            ele_floor_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_floor_list_num')
            list_floor_num = [ele_floor_num[i].get_attribute('text') for i in range(len(ele_floor_num))]
            # 通过层号获取层号的索引值
            floor_index = list_floor_num.index(str(floor_num))
            is_checked = ele_check_floor[floor_index].get_attribute('checked')
            # 层注册/去注册
            if is_register[2]:
                if is_checked != 'true':
                    ele_check_floor[floor_index].click()
            else:
                if is_checked == 'true':
                    ele_check_floor[floor_index].click()
            # 重新获取层的注册信息
            ele_check_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_floor_list_register')
            is_floor_checked = ele_check_floor[floor_index].get_attribute('checked')
            is_floor_register = func(is_floor_checked)  # 层号是否已被注册
            result['is_floor_reg'] = is_floor_register
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_list_save_btn').click()
        self.clog(get_current_info() + "Location is_register. args: {'comm_num': %s, 'comm_locate': %s, "
                                       "'build_num': %s, 'build_locate': %s, 'floor_num': %s, 'is_save': %s, 'is_register': %s}"
                  % (comm_num, comm_locate, build_num, build_locate, floor_num, is_save, is_register))
        return result

    def app_get_location(self, comm_num=None, build_num=None, floor_num=None):
        """
        获取区栋层的状态信息，如获取是否注册的信息、获取位置信息
        :param comm_num: 区号
        :param build_num: 栋号
        :param floor_num: 层号
        :return: 区栋层是否注册及区栋的位置信息
        ret = {'is_comm_reg': bool, 'is_build_reg': bool, 'is_floor_reg': bool, 'comm_loc': str, 'build_loc': str, 'list_comm_num':list（当页显示区号列表）,
        'list_build_num': list(当页显示栋号列表)
        """
        func = lambda x: True if x == 'true' else False  # 判断属性值是否为‘true'
        ret = {}
        if comm_num:
            # 区选择框
            ele_check_comm = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_register')
            # 区号控件集
            ele_comm_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_num')
            list_comm_num = [ele_comm_num[i].get_attribute('text') for i in range(len(ele_comm_num))]  # 区号列表
            ret['list_comm_num'] = list_comm_num
            comm_index = list_comm_num.index(str(comm_num))  # 通过区号获取区号所在控件的索引值
            is_comm_checked = ele_check_comm[comm_index].get_attribute('checked')
            is_comm_register = func(is_comm_checked)  # 区号是否被注册
            ret['is_comm_reg'] = is_comm_register
            # 获取区位置信息
            ele_check_comm_loc = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_community_list_desc')
            comm_loc = ele_check_comm_loc[comm_index].get_attribute('text')
            ret['comm_loc'] = comm_loc
        if build_num:
            # 栋选择框
            ele_check_build = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_register')
            # 栋号控件集
            ele_build_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_num')
            list_build_num = [ele_build_num[i].get_attribute('text') for i in range(len(ele_build_num))]  # 栋号列表
            ret['list_build_num'] = list_build_num
            build_index = list_build_num.index(str(build_num))  # 栋号索引
            is_build_checked = ele_check_build[build_index].get_attribute('checked')
            is_build_register = func(is_build_checked)  # 栋号是否被注册
            ret['is_build_reg'] = is_build_register
            # 栋位置信息
            ele_check_build_loc = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_building_list_desc')
            build_loc = ele_check_build_loc[build_index].get_attribute('text')
            ret['build_loc'] = build_loc
        if floor_num:
            # 层选择框
            ele_check_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_floor_list_register')
            # 层号
            ele_floor_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location_floor_list_num')
            list_floor_num = [ele_floor_num[i].get_attribute('text') for i in range(len(ele_floor_num))]
            ret['list_floor_num'] = list_floor_num
            # 通过层号获取层号的索引值
            floor_index = list_floor_num.index(str(floor_num))
            is_floor_checked = ele_check_floor[floor_index].get_attribute('checked')
            is_floor_register = func(is_floor_checked)  # 层号是否已被注册
            ret['is_floor_reg'] = is_floor_register
        return ret

    def app_location_batch_register(self, batch_text, tap_loc=None, is_register=True, is_submit=True):
        """
        批量注册区栋层
        :param batch_text: 批量操作文本，如：区注册、栋注册、层注册
        :param tap_loc: 目标区号/栋号/层号的坐标，如目标区号为3， 则坐标为（1040,620）
        :param is_register:是否注册
        :param is_submit: 是否确定
        :return:
        """
        # 点击批操作
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_list_batches_operation_btn').click()
        self.driver.find_element_by_name(batch_text).click()
        checkbox = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_checkbox')
        is_checked = checkbox.get_attribute('checked')
        if tap_loc:
            sleep(3)
            self.driver.tap([tap_loc])
        if is_register:
            if is_checked != 'true':
                checkbox.click()
        else:
            if is_checked == 'true':
                checkbox.click()
        if is_submit:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_cancel').click()

    def app_location_batch_register_desc(self, batch_text, tap_loc=None, location=None, is_submit=True):
        """
                批量注册区位置或栋位置
                :param batch_text: 批量操作文本，如：区位置、栋位置
                :param tap_loc: 目标区号/栋号的坐标，如目标区号为3， 则坐标为(880,620)
                :param location: 位置秒速
                :param is_submit: 是否确定
                :return:
                """
        # 点击批操作
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_list_batches_operation_btn').click()
        self.driver.find_element_by_name(batch_text).click()
        if tap_loc:
            sleep(3)
            self.driver.tap([tap_loc])
        if location:
            ele_desc = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_description_edit')
            ele_desc.click()
            ele_desc.clear()
            ele_desc.send_keys(location)
            self.driver.hide_keyboard()
        if is_submit:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_description_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_description_cancel').click()

    def app_swipe_loops(self, start_x, start_y, end_x, end_y, times):
        """
        循环上下滑动
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
         - times - the times of repeat swipe / number of repeated slips

        :Usage:
            sj.app_swipe_loops(100, 100, 100, 400, 10)
        :return: None
        """
        for i in range(times):
            # duration: if slip slow
            self.driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=1000)

    def app_device_loopboard(self, board_num=None, is_register=True, is_save=False):
        """
        回路板设置
        :param board_num: int 回路板号
        :param is_register: bool 是否注册
        :param is_save: bool 是否保存设置
        :return:
        """
        if board_num:
            # 根据回路板名获取回路板的索引位置
            for i in range(8):
                ele_board_name = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/interface_board_setting_name')
                list_board_name = [ele_board_name[i].get_attribute('text') for i in range(len(ele_board_name))]
                if str(board_num) in list_board_name:
                    break
                else:
                    self.driver.swipe(start_x=500, start_y=796, end_x=500, end_y=360, duration=1000)
            board_index = list_board_name.index(str(board_num))
            ele_board_reg = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/interface_board_setting_register')
            is_checked = ele_board_reg[board_index].get_attribute('checked')
            # 注册
            if is_register:
                if is_checked != 'true':
                    ele_board_reg[board_index].click()
            else:
                if is_checked == 'true':
                    ele_board_reg[board_index].click()
        # 保存
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/local_device_save_btn').click()
        self.clog(get_current_info() + 'Rigester interface board. board_num: %s. is_register: %s. is_save: %s' % (board_num, is_register, is_save))

    def app_get_device_loopboard(self, board_num=None):
        """
        获取回路板的状态信息
        :param board_num: int 回路板号
        :return: {'list_board_name'：list_board_name （board_num所在页的所有回路板号）
        ‘is_register': is_register board_num是否注册}
        """
        ret = dict()
        # 根据回路板名获取回路板的索引位置
        for j in range(8):
            ele_board_name = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/interface_board_setting_name')
            list_board_name = [ele_board_name[i].get_attribute('text') for i in range(len(ele_board_name))]
            if str(board_num) in list_board_name:
                break
            else:
                self.driver.swipe(start_x=500, start_y=796, end_x=500, end_y=360, duration=1000)
        ret['list_board_name'] = list_board_name
        if board_num:
            board_index = list_board_name.index(str(board_num))
            ele_board_reg = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/interface_board_setting_register')
            is_checked = ele_board_reg[board_index].get_attribute('checked')
            is_register = True if is_checked == 'true' else False
            ret['is_register'] = is_register
        return ret

    def app_loopboard_batch_register(self, tap_loc, is_register=True, is_submit=True):
        """
        批量注册回路板
        :param tap_loc: [(666.625), (1028, 625)] 点击坐标，如从3号回路板(666,625)到5号回路板(1028,625)、(1028,625)
        :param is_register:
        :param is_submit:
        :return:
        """
        # 点击批量注册
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/interface_board_batches_operation_btn').click()
        checkbox = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_checkbox')
        is_checked = checkbox.get_attribute('checked')
        if tap_loc:
            # 点击tap_loc里的每个坐标
            for loc in tap_loc:
                sleep(3)
                self.driver.tap([loc])
        if is_register:
            if is_checked != 'true':
                checkbox.click()
        else:
            if is_checked == 'true':
                checkbox.click()
        if is_submit:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_confirm').click()
        else:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_batches_register_shield_cancel').click()
        self.clog(get_current_info() + 'Batch register board. tap_loc: %s. is_register: %s. is_submit: %s' % (tap_loc, is_register, is_submit))

    def app_terminal(self, loop_num, is_setting=True):
        """
        终端设置界面点击进入详细设置或点击自动登录，控件：详细设置 自动登录
        :param loop_num: int 回路号
        :param is_setting: bool 是否进入详细设置，若为False则点击自动登录
        :return:
        """
        # item的个数
        ele_items = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_item')
        # 如果界面信息显示不完整，即出现6个回路板，则丢弃首尾，只剩中间4个完整的回路板
        if len(ele_items) != 5:
            ele_items.pop(0)
            ele_items.pop()
        ele_loop_name = list()
        ele_loop_detail = list()
        ele_loop_auto = list()
        for ele_item in ele_items:
            # 回路号
            ele_loop_name.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_name'))
            ele_loop_name.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_name'))
            # 详细设置
            ele_loop_detail.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_detail'))
            ele_loop_detail.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_detail'))
            # 自动登录
            ele_loop_auto.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_auto'))
            ele_loop_auto.append(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_auto'))
        # 获取当前界面的回路号
        loop_name = [int(i.get_attribute('text')) for i in ele_loop_name]
        if loop_num in loop_name:
            loop_index = loop_name.index(loop_num)      # 回路号的索引位置
            if is_setting:
                ele_loop_detail[loop_index].click()     # 点击详细设置
            else:
                ele_loop_auto[loop_index].click()       # 点击自动登录
        else:
            # 从下往上滑
            pass
        self.clog(get_current_info() + 'Detail setting or auto logging. loop num: %s. is detail setting: %s' % (loop_num, is_setting))

    def app_get_terminal(self, loop_num):
        """
        获取终端设置界面的信息 如：回路板(int)，回路号(int)，终端数(int)，是否注册(0 or 1)
        :param loop_num:
        :return: [回路板，回路号， 终端数，是否自动登录] = [int, int, int, int(0或者1)]
        """
        # item的个数
        ele_items = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_item')
        # 如果界面信息显示不完整，即出现6个回路板，则丢弃首尾，只剩中间4个完整的回路板
        if len(ele_items) != 5:
            ele_items.pop(0)
            ele_items.pop()
        list_lines = list()
        board_num = list()
        for ele_item in ele_items:
            list_line = list()
            # 回路板
            list_line.append(int(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_interface_board_name').get_attribute('text')))
            # 回路号、终端数、自动登录（若可以自动登录则为1， 否则为0）
            list_line.append(int(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_name').get_attribute('text')))
            list_line.append(int(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_count').get_attribute('text')))
            one_auto = ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_one_auto').get_attribute('text')
            is_auto = 1 if one_auto == u'自动登录' else 0
            list_line.append(is_auto)
            list_line.append(int(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_name').get_attribute('text')))
            list_line.append(int(ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_count').get_attribute('text')))
            two_auto = ele_item.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_setting_loop_two_auto').get_attribute('text')
            is_auto = 1 if two_auto == u'自动登录' else 0
            list_line.append(is_auto)
            # 回路号
            board_num.append(list_line[0])
            list_lines.append(list_line)
        if ((loop_num+1)//2) in board_num:
            board_index = board_num.index((loop_num+1)//2)      # 回路板号对应的索引位置
            result_line = list_lines[board_index]
            # 按回路号所在的行返回整行信息
            if loop_num % 2 == 1:
                result = result_line[:4]
            else:
                result = [result_line[0]]+ result_line[-1:-4]
            return result
        else:
            # 从下往上滑
            pass

    def app_terminal_setting_basic(self, terminal_num, is_batch=False, is_register=False, is_shield=False, is_save=False):
        """
        终端设置是否注册、是否屏蔽
        :param terminal_num: 单个注册时：int 终端号。批量注册时：tuple 终端号(start, end)
        :param is_batch: bool 是否批量注册，True则批量注册terminal为tuple，False则单个注册，termianl为int
        :param is_register: bool 是否注册
        :param is_shield:  bool 是否屏蔽
        :param is_save:  bool 是否保存
        :return:
        """
        if is_batch:
            if self.app_is_display('清除批量选择'):
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_clear_btn').click()
            else:
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_batches_operation_btn').click()
            for i in range(terminal_num[0], terminal_num[1]):
                self.driver.find_element_by_name(str(i)).click()
        else:
            try :
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_clear_btn')
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_batches_operation_btn').click()
            except:
                pass
            self.driver.find_element_by_name(str(terminal_num)).click()
        if is_register:
            ele_register = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_register')
            is_checked = ele_register.get_attribute('checked')
            if is_checked != 'true':
                ele_register.click()
        if is_shield:
            ele_shield = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_shield')
            is_checked = ele_shield.get_attribute('checked')
            if is_checked != 'true':
                ele_shield.click()
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_view_save_btn').click()

    def app_linkage_terminal_setting_info(self, terminal_num, is_batch=False, device_type=None, product=None, location=None, locat_desc=None, more=None, is_save=False):
        """
        终端设置类型、位置等
        :param terminal_num: 单个注册时：int 终端号。批量注册时：tuple 终端号(start, end)
        :param is_batch: bool 是否批量注册，True则批量注册terminal为tuple，False则单个注册，termianl为int
        :param device_type: str 设备类型
        :param product: str 生产类型
        :param location: tuple 区栋层房，如:1区1栋1层1房(1,1,1,1)
        :param locat_desc: str 位置
        :param more: 点击更多
        :param is_save： 是否保存
        :return:
        """
        if is_batch:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_batches_operation_btn').click()
            for i in range(terminal_num[0], terminal_num[1]):
                self.driver.find_element_by_name(str(i)).click()
        else:
            self.driver.find_element_by_name(str(terminal_num)).click()
        if device_type:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_type_btn').click()
            self.driver.find_element_by_name(device_type).click()
        if product:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_product_btn').click()
            self.driver.find_element_by_name(product).click()
        # 暂不支持上下滑动
        if location:
            location = [str(location[i]) for i in location]
            # 编辑区栋房层
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_location_btn').click()
            # 选择区1 - 7
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_location_community_spinner').click()
            self.driver.find_element_by_name(location[0])
            # 选择栋 1 - 7
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_location_building_spinner').click()
            self.driver.find_element_by_name(location[1])
            # 选择层 1 - 7
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_location_floor_spinner').click()
            self.driver.find_element_by_name(location[2])
            # 选择房 1 - 7
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_location_room_spinner').click()
            self.driver.find_element_by_id(location[3])
        if locat_desc:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_description_btn').click()
            ele_edit = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_change_description_edit')
            ele_edit.send_keys('abccdd')
        if more:
            # 点击更多
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_more_btn').click()
        if is_save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_view_save_btn').click()

    def app_get_terminal_setting(self, terminal_num):
        """获取终端设置回路点的详细设置界面的信息"""
        self.driver.find_element_by_name(str(terminal_num)).click()
        val_register = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_register').get_attribute('checked')
        is_register = True if val_register == 'true' else False
        val_shield = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_shield').get_attribute('checked')
        is_shield = True if val_shield == 'true' else False
        device_type = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_type_tx').get_attribute('text')
        product_type = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_product_tx').get_attribute('text')
        location = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_location_tx').get_attribute('text')
        desc = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_description_btn').get_attribute('text')
        normal_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_normal_count').get_attribute('text')
        fire_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_fire_count').get_attribute('text')
        fault_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_fault_count').get_attribute('text')
        startup_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_startup_count').get_attribute('text')
        feedback_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_feedback_count').get_attribute('text')
        shield_count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/terminal_detail_grid_modify_shield_count').get_attribute('text')
        return {'is_register':is_register, 'is_shield': is_shield, 'device_type':device_type, 'product_type':product_type, 'location':location,
                'desc':desc, 'normal_count':normal_count, 'fire_count':fire_count, 'fault_count': fault_count, 'startup_count':startup_count,
                'feedback_count': feedback_count, 'shield_count':shield_count, }

if __name__ == "__main__":
    sj = Controller()
