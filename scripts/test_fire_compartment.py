"""
    防火分区
"""
import sys
sys.path.append('..')
from libs import *
import unittest


class TestFireCompartment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sj = Fire_Compartment()

    def setUp(self):
        self.sj.driver.implicitly_wait(5)

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                flag = self.sj.app_is_main_page()
            except:
                pass

    def test_fire_comp_324_0(self):
        """
        324：添加一个防火分区，3区4栋1层~2层1房~10房，生效，位置
        329：查看防火分区：任意点击一条记录进行查看，不修改设置，点击返回或者保存
        """
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('fire_compartment')
        self.sj.fire_compartment_btn('add')
        sleep(1)
        self.sj.fire_compartment_add(comp_locate=3, comp_build=4, comp_floor1=2, comp_room=(1, 10), comp_decs='abc', is_batch=True)
        # 通过点击房号，进入修改防火分区信息
        ele_rooms = self.sj.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_room')
        # 不做修改，点击返回
        ele_rooms[0].click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_back_btn').click()
        # 不做修改，点击保存
        ele_rooms[0].click()
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_save').click()
        location = self.sj.fire_compartment_get_info(1).get('location')
        self.assertTrue(location, '3区4栋1层 ~ 2层')
        # 取消删除防火分区
        self.sj.fire_compartment_btn('delete')
        self.sj.app_is_display('确定删除当前防火分区？')
        self.sj.fire_compartment_dialog('cancel')
        self.assertTrue(location, '3区4栋1层 ~ 2层')
        # 确认删除该防火分区
        self.sj.fire_compartment_btn('delete')
        self.sj.app_is_display('确定删除当前防火分区？')
        self.sj.fire_compartment_dialog('confirm')

    def test_fire_comp_327_0(self):
        """判断防火分区列表中生效功能是否有效"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('fire_compartment')
        self.sj.fire_compartment_btn('add')
        sleep(1)
        self.sj.fire_compartment_add(comp_floor1=2, comp_room=1, comp_decs='efg')
        # 获取防火分区信息
        comp_result = self.sj.fire_compartment_order(1)
        is_order = comp_result.get('is_order')
        try:
            # 当前状态是生效的
            if is_order == 'true':
                self.assertTrue(self.sj.app_is_display('确定使当前防火分区失效?'))
                self.sj.driver.find_element_by_name('取消').click()
                result = self.sj.fire_compartment_get_order(1)
                self.assertEqual(result.get('is_order'), is_order)
                # 失效之后，判断和之前的结果是否相同
                self.sj.fire_compartment_order(1)
                self.assertTrue(self.sj.app_is_display('确定使当前防火分区失效?'))
                self.sj.driver.find_element_by_name('确定').click()
                result = self.sj.fire_compartment_get_order(1)
                self.assertNotEqual(result.get('is_order'), is_order)
                # 还原环境
                self.sj.fire_compartment_order(1)
                self.sj.driver.find_element_by_name('确定').click()
            elif is_order == 'false':
                self.assertTrue(self.sj.app_is_display('确定使当前防火分区生效?'))
                self.sj.driver.find_element_by_name('取消').click()
                result = self.sj.fire_compartment_get_order(1)
                self.assertEqual(result.get('is_order'), is_order)
                # 生效之后，判断和之前的结果是否相同
                self.sj.fire_compartment_order(1)
                self.assertTrue(self.sj.app_is_display('确定使当前防火分区生效?'))
                self.sj.driver.find_element_by_name('确定').click()
                result = self.sj.fire_compartment_get_order(1)
                self.assertNotEqual(result.get('is_order'), is_order)
                # 还原测试环境
                self.sj.fire_compartment_order(1)
                self.sj.driver.find_element_by_name('确定').click()
        finally:
            self.sj.fire_compartment_btn('delete')
            self.sj.fire_compartment_dialog('confirm')

    def test_fire_compartment_330(self):
        """进行添加、修改、删除防火分区后，分别对照操作记录"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu('fire_compartment')
        self.sj.fire_compartment_btn('add')
        sleep(1)
        self.sj.fire_compartment_add(comp_locate=2, comp_build=3, comp_floor1=3, comp_room=(1, 5), comp_decs='pml', is_batch=True)
        # 通过点击房号，进入修改防火分区信息
        ele_rooms = self.sj.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_room')
        ele_rooms[0].click()
        self.sj.fire_compartment_add(comp_room=5)
        sleep(1)
        self.sj.fire_compartment_delete(1).click()
        self.sj.app_is_display('确定删除当前防火分区？')
        self.sj.fire_compartment_dialog('confirm')
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_back_btn').click()
        self.sj.app_menu(menu_id='query', is_click_menu=False)
        self.sj.app_query('operation')
        record1 = self.sj.app_query_history(record_num=1, record_type='operation')
        self.assertEqual(record1[2], u'删除防火分区(区栋层：2区3栋1层 ~ 3层；位置：pml)')
        self.assertEqual(record1[3], u'系统管理员')  # 用户
        self.assertEqual(record1[4], u'系统管理员')  # 用户类型
        record2 = self.sj.app_query_history(record_num=2, record_type='operation')
        self.assertEqual(record2[2], u'修改防火分区(区栋层：2区3栋1层 ~ 3层；房间数 ：4；位置：pml；生效：true)')
        record3 = self.sj.app_query_history(record_num=3, record_type='operation')
        self.assertEqual(record3[2], u'添加防火分区(区栋层：2区3栋1层 ~ 3层；房间数 ：5；位置：pml；生效：true)')
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/system_history_back_btn').click()


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # run_suite(TestFireCompartment)