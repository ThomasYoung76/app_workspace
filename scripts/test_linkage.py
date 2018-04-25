"""
    联动设置
"""
import sys
sys.path.append('..')
from libs import *
import unittest
from parameterized import parameterized


class TestLinkage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sj = Linkage()

    def setUp(self):
        self.sj.driver.implicitly_wait(5)

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

    def test_linkage_336_0(self):
        """联动设置, 联动原则选择界面1和界面2，未注册区栋层时，进行添加 不选，单选，全选"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击联动原则
        self.sj.linkage_add(0)
        # 不选
        self.sj.linkage_principle_choose(index=0, is_make=False)
        self.sj.linkage_principle_choose(index=0, is_make=True)
        # 单选栋联动
        self.sj.linkage_principle_choose(index=0, is_make=True)
        count = self.sj.linkage_principle_make_get_count(area=0)
        self.assertEqual(count, (27, 27))
        # 单选邻层联动
        self.sj.linkage_principle_choose_btn('previous')
        self.sj.linkage_principle_choose(index=0, is_make=False)   # 取消选择栋联动
        self.sj.linkage_principle_choose(index=6, is_make=True)
        count = self.sj.linkage_principle_make_get_count(area=1)
        self.assertEqual(count, (3, 3))
        # 单选层联动
        self.sj.linkage_principle_choose_btn('previous')
        self.sj.linkage_principle_choose(index=6, is_make=False)   #取消邻层联动
        self.sj.linkage_principle_choose(index=7, is_make=True)
        count = self.sj.linkage_principle_make_get_count(area=2)
        self.assertEqual(count, (1, 1))
        # 点击返回，重新添加并全选
        self.sj.linkage_principle_choose_btn('back')
        self.sj.linkage_list_btn('add')
        self.sj.linkage_add(0)
        self.sj.linkage_principle_choose(is_choose_all=True)
        self.sj.linkage_principle_choose_btn('make')
        count_0 = self.sj.linkage_principle_make_get_count(area=0)
        count_1 = self.sj.linkage_principle_make_get_count(area=1)
        count_2 = self.sj.linkage_principle_make_get_count(area=2)
        self.assertEqual(count_0, (27, 27))
        self.assertEqual(count_1, (3, 3))
        self.assertEqual(count_2, (1, 1))
        # 保存
        self.sj.linkage_principle_choose_btn('save')
        # 检查联动数正确
        count = self.sj.linkage_get_list_count()
        self.assertEqual(count, 31)
        # 全部删除
        self.sj.linkage_list_btn('delete')
        self.sj.linkage_list_btn_confirm(True)
        self.sj.linkage_list_btn('back')

    def test_linkage_336_1(self):
        """联动条目预览：①全选、②取消全选、③手动选择/取消选择、④返回"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击联动原则
        self.sj.linkage_add(0)
        # 单选邻层联动并预览
        self.sj.linkage_principle_choose(index=6, is_make=True)
        self.sj.linkage_principle_make_get_count(area=1, is_preview=True)
        count_link, count_reg = self.sj.linkage_principle_preview()
        # 取消选择
        count_link, count_reg_none = self.sj.linkage_principle_preview(is_select_none=True)
        # 手动选择第3条
        self.sj.linkage_principle_preview_get_status(index=2, is_click=True)
        count_link, count_reg_1 = self.sj.linkage_principle_preview()
        # 全选
        count_link, count_reg_all = self.sj.linkage_principle_preview(is_select_all=True)
        # 取消选择第1条
        self.sj.linkage_principle_preview_get_status(index=0, is_click=True)
        count_link, count_reg_2 = self.sj.linkage_principle_preview()
        # 检查
        self.assertEqual(count_reg, 3)
        self.assertEqual(count_reg_none, 0)
        self.assertEqual(count_reg_1, 1)
        self.assertEqual(count_reg_2, 2)
        self.assertEqual(count_reg_all, 3)
        # 返回并保存
        self.sj.linkage_principle_choose_btn('back')
        # 保存
        self.sj.linkage_principle_choose_btn('save')
        # 检查联动数正确
        count = self.sj.linkage_get_list_count()
        self.assertEqual(count, 2)
        # 全部删除
        self.sj.linkage_list_btn('delete')
        self.sj.linkage_list_btn_confirm(True)
        self.sj.linkage_list_btn('back')

    @parameterized.expand(input=param_linkage_index)
    def test_linkage_339_349_359_391_371_381(self, index):
        """联动 ->>> 进入“选择输入条件”界面"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击xxx联动
        self.sj.linkage_add(index)
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        # 选择火警输入的终端相应的图标
        list_selected_term = self.sj.linkage_edit_input_condition(index=[0, 1, 2, 3])
        self.assertEqual(list_selected_term[0], '光电探测器')
        self.assertEqual(list_selected_term[1], '感温探测器')
        self.assertEqual(list_selected_term[2], '广播')
        self.assertEqual(list_selected_term[3], '手动按钮')
        # 再次选择同一类火警输入的图标
        list_selected_term = self.sj.linkage_edit_input_condition(index=[0])
        self.assertNotEqual(list_selected_term[0], '光电探测器')
        # 点击已选择框内的删除图标
        list_selected_term = self.sj.linkage_edit_input_condition(del_num=[0])
        self.assertNotEqual(list_selected_term[0], '感温探测器')
        self.assertEqual(list_selected_term[0], '广播')
        # 点击已选择框内的全部删除
        list_selected_term = self.sj.linkage_edit_input_condition(is_del_all=True)
        self.assertFalse(list_selected_term)
        # 再次添加一类火警终端，默认条件是条件相或，选择保存
        self.sj.linkage_edit_input_condition(index=[0], save='confirm')
        # 点击编辑输入条件后，选择取消
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition(save='cancel')
        # 判断输入条件是否仍为原来的状态
        input_result = self.sj.linkage_get_input_condition()
        self.assertEqual(input_result[0], '编辑输入条件(1)')
        self.assertEqual(input_result[1], '条件相或')
        self.assertEqual(input_result[2][0], '光电探测器')
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition(condition='and', save='confirm')
        value = self.sj.linkage_get_input_condition()[1]
        self.assertEqual(value, '条件相与')
        # 还原测试环境
        self.sj.linkage_interface_choose_btn('back_btn')

    @parameterized.expand(input=param_linkage_block_index + [(7,)])
    def test_linkage_340_350_360_392_402(self, index):
        """联动 ->>> 进入“选择输出结果”界面"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击xxx联动
        self.sj.linkage_add(index)
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn('right_click')
        # 选择设备类型、回路、区栋层
        list_selected_result = self.sj.linkage_edit_output_result(loop='v2 (虚拟回路板)', community='1', building='1')
        # 判断筛选的条件，显示出来的是否正确
        location_result = list_selected_result[1]
        comm = location_result[0][0]
        build = location_result[0][2]
        self.assertEqual(comm, '1')
        self.assertEqual(build, '1')
        # list_wait_selected_result[2] ->>> debug code
        debug_code_result = list_selected_result[2]
        debug_code = debug_code_result[0][4:6]
        self.assertEqual(debug_code, '82')
        # 点击清除筛选条件
        all_result = self.sj.linkage_edit_output_result(is_clear_filter=True)
        self.assertEqual(all_result, [[], [], []])
        # 再次选择回路
        self.sj.linkage_edit_output_result(loop='v2 (虚拟回路板)')
        # 选择设备类型
        list_result = self.sj.linkage_edit_output_result(index=[0, 1, 2])
        debug_code_result = list_result[2]
        debug_code_result_len1 = len(debug_code_result)
        self.assertEqual(debug_code_result[0], debug_code_result[7])
        # 多次选择同一个设备类型，状态在选择和移除间切换
        list_result = self.sj.linkage_edit_output_result(index=[0])
        debug_code_result = list_result[2]
        self.assertEqual(debug_code_result[7], '001-82-002')
        debug_code_result_len2 = len(debug_code_result)
        self.assertNotEqual(debug_code_result_len1, debug_code_result_len2)
        # 全选
        self.sj.linkage_edit_output_result(is_select_all=True)
        # 全选之后，滑动到最底，比较两边最后一条数据是否一样
        self.sj.app_swipe_loops(start_x=359, start_y=771, end_x=359, end_y=405, times=56)
        self.sj.app_swipe_loops(start_x=1137, start_y=749, end_x=1137, end_y=261, times=54)
        debug_code_result = self.sj.linkage_edit_output_result()[2]
        self.assertEqual(debug_code_result[6], debug_code_result[15])
        # 单个删除已选的设备类型 ->>> del_num下标范围[0~8]
        code_result = self.sj.linkage_edit_output_result(del_num=[8])
        self.assertNotEqual(code_result[2][15], '001-82-324')
        # 全部删除已选的设备类型
        debug_code_result = self.sj.linkage_edit_output_result(is_del_all=True)
        self.assertEqual(len(debug_code_result[0]), 7)
        # 再一次选择同一个设备类型，状态在选择和移除间切换，保存
        self.sj.linkage_edit_output_result(index=[1], save='confirm')
        # 获取系统联动输出结果信息
        output_result = self.sj.linkage_get_output_result()
        self.assertEqual(output_result[0], '编辑输出结果(1)')
        self.assertEqual(output_result[5][0], '001-82-319')
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn('right_click')
        # 点击取消，查看输出结果内容是否会改变
        self.sj.linkage_edit_output_result(save='cancel')
        output_result = self.sj.linkage_get_output_result()
        self.assertEqual(output_result[5][0], '001-82-319')
        # 还原测试环境
        self.sj.linkage_interface_choose_btn('back_btn')

    @parameterized.expand(input=param_linkage_block_index)
    def test_linkage_338_348_358_390_347_357_367_399(self, index):
        """添加一条联动信息"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击系统联动
        self.sj.linkage_add(index)
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition(index=[0, 1], save='confirm')
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn('right_click')
        # 选择设备类型、回路、区栋层
        self.sj.linkage_edit_output_result(loop='v1 (虚拟回路板)', index=[0, 1], save='confirm')
        # 通过点击“编辑输入条件”进入“选择输入条件”界面，再取消退出
        self.sj.linkage_interface_choose_btn('edit_input')
        self.sj.linkage_edit_input_condition(save='cancel')
        # 通过点击“编辑输出结果”进入“选择输出结果”界面，再取消退出
        self.sj.linkage_interface_choose_btn(button='edit_output')
        self.sj.linkage_edit_output_result(save='cancel')
        # 选择至少报警个数，以火警个数传参数
        self.sj.linkage_interface_choose_btn(button='limit_alarm_spinner', limit_alarm=1)
        if index == 2:
            # 更改联动范围
            self.sj.linkage_interface_choose_btn(button='input_range_change_btn')
            self.sj.linkage_input_range_change(community=3, save='confirm', coordinate=[[885, 741, 885, 507]])
        elif index == 3:
            # 更改联动范围
            self.sj.linkage_interface_choose_btn(button='input_range_change_btn')
            self.sj.linkage_input_range_change(community=2, building=3, startfloor=4, endfloor=8, save='confirm',
                                               coordinate=[[581, 741, 581, 507], [785, 741, 785, 507],
                                                           [989, 741, 989, 507], [1189, 741, 1189, 507]])
        elif index == 6:
            # 更改联动范围
            self.sj.linkage_interface_choose_btn(button='input_range_change_btn')
            self.sj.linkage_input_range_change(community=2, building=3, startfloor=3, startroom=4, endroom=25,
                                               save='confirm',
                                               coordinate=[[479, 741, 479, 507], [683, 741, 683, 507],
                                                           [887, 741, 887, 507], [1091, 741, 1091, 507],
                                                           [1291, 741, 1291, 507]])
        # 输出延时，是否生效
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
        self.sj.linkage_edit_input_condition(index=[0, 1, 2], save='confirm')
        self.sj.linkage_interface_choose_btn(save='save_continue_add_btn')
        input_result = self.sj.linkage_get_input_condition()
        self.assertEqual(input_result[1], '条件相或')
        self.sj.linkage_interface_choose_btn(button='back_btn')
        result = self.sj.linkage_get_list_information()
        self.assertEqual(result[3][0], '广播 ')  # 定位到的“广播”后面带有空格
        # 全部删除
        self.sj.linkage_list_btn('delete')
        self.sj.linkage_list_btn_confirm(True)

    @parameterized.expand(input=param_linkage_layer_index)
    def test_linkage_370_380(self, index):
        """添加一条联动信息"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        self.sj.linkage_add(index)
        input_output_range = self.sj.linkage_get_output_result()[6]
        if index == 4:
            self.assertEqual(input_output_range, '输入与输出范围：输入与输出在同一层')
        elif index == 5:
            self.assertEqual(input_output_range, '输入与输出范围：无')
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn(button='left_click')
        self.sj.linkage_edit_input_condition(index=[0, 1], save='confirm')
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn(button='right_click')
        self.sj.linkage_edit_output_result_layer(index=[0, 1, 2], save='confirm')
        # 通过点击“编辑输入条件”进入“选择输入条件”界面，再取消退出
        self.sj.linkage_interface_choose_btn(button='edit_input')
        self.sj.linkage_edit_input_condition(save='cancel')
        # 通过点击“编辑输出结果”进入“选择输出结果”界面，再取消退出
        self.sj.linkage_interface_choose_btn(button='edit_output')
        self.sj.linkage_edit_output_result(save='cancel')
        if index == 5:
            # 选择至少报警个数 和 启动邻层
            self.sj.linkage_interface_choose_btn(button='limit_alarm_spinner', limit_alarm=1)
            # 更改输入与输出范围
            self.sj.linkage_interface_choose_btn(button='input_range_change_btn')
            self.sj.linkage_input_range_change(community=2, building=3, startfloor=4, endfloor=8, save='confirm',
                                               coordinate=[[581, 741, 581, 507], [785, 741, 785, 507],
                                                           [989, 741, 989, 507], [1189, 741, 1189, 507]])
        else:
            self.sj.linkage_interface_choose_btn(button='limit_alarm_spinner', limit_alarm=1, is_adjacent=True)
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
        self.sj.linkage_edit_input_condition(index=[0, 1, 2], save='confirm')
        self.sj.linkage_interface_choose_btn(save='save_continue_add_btn')
        input_result = self.sj.linkage_get_input_condition()
        self.assertEqual(input_result[1], '条件相或')
        self.sj.linkage_interface_choose_btn(button='back_btn')
        result = self.sj.linkage_get_list_information()
        self.assertEqual(result[3][0], '广播 ')  # 定位到的“广播”后面带有空格
        # 全部删除
        self.sj.linkage_list_btn('delete')
        self.sj.linkage_list_btn_confirm(True)

    @parameterized.expand(input=param_linkage_layer_index)
    def test_linkage_372_382(self, index):
        """层中联动 ->>> 进入“选择输入条件”界面"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        # 未注册区栋层时进行添加
        self.sj.linkage_list_btn('add')
        # 点击层中联动
        self.sj.linkage_add(index)
        # 点击编辑输出结果
        self.sj.linkage_interface_choose_btn('right_click')
        # 选择输出结果相应的图标
        list_selected_term = self.sj.linkage_edit_output_result_layer(index=[0, 1, 2, 3])
        self.assertEqual(list_selected_term[0], '声光警报器')
        self.assertEqual(list_selected_term[1], '广播')
        self.assertEqual(list_selected_term[2], '远音')
        self.assertEqual(list_selected_term[3], '排烟阀')
        # 多次重复选择同一个设备类型
        list_selected_term = self.sj.linkage_edit_output_result_layer(index=[0])
        self.assertNotEqual(list_selected_term[0], '声光警报器')
        # 单个删除已选的设备类型
        list_selected_term = self.sj.linkage_edit_output_result_layer(del_num=[0])
        self.assertNotEqual(list_selected_term[0], '广播')
        self.assertEqual(list_selected_term[0], '远音')
        # 全部删除已选的设备类型
        list_selected_term = self.sj.linkage_edit_output_result_layer(is_del_all=True)
        self.assertFalse(list_selected_term)
        # 再次添加一输出类型，选择保存
        self.sj.linkage_edit_output_result_layer(index=[0], save='confirm')
        # 点击编辑输出结果后，选择取消
        self.sj.linkage_interface_choose_btn('right_click')
        self.sj.linkage_edit_input_condition(save='cancel')
        # 判断输出结果是否仍为原来的状态
        output_result = self.sj.linkage_get_output_result()
        self.assertEqual(output_result[0], '编辑输出结果(1)')
        self.assertEqual(output_result[3][0], '声光警报器')
        # 还原测试环境
        self.sj.linkage_interface_choose_btn('back_btn')

    def test_linkage_401(self):
        """复合联动 ->>> 进入“选择输入条件”界面"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='linkage')
        self.sj.linkage_list_btn('add')
        self.sj.linkage_add(7)
        # 点击编辑输入条件
        self.sj.linkage_interface_choose_btn('left_click')
        # 选择主机，回路，地址号
        list_selected_term = self.sj.linkage_edit_input_condition_compound(host=2, loop=1, device_addr=3, is_add=True)
        self.assertEqual(list_selected_term[0], '2主机41回路板81回路3号')
        # 再次选择主机，回路，地址号
        self.sj.linkage_edit_input_condition_compound(host=3, loop=2, device_addr=5, is_add=True)
        # 点击已选择框内的删除图标
        list_selected_term = self.sj.linkage_edit_input_condition_compound(del_num=[0])
        self.assertNotEqual(list_selected_term[0], '2主机41回路板81回路3号')
        self.assertEqual(list_selected_term[0], '3主机41回路板82回路5号')
        # 点击已选择框内的全部删除
        list_selected_term = self.sj.linkage_edit_input_condition_compound(is_del_all=True)
        self.assertFalse(list_selected_term)
        # 再次选择主机，回路，地址号
        self.sj.linkage_edit_input_condition_compound(host=1, loop=3, device_addr=20, is_add=True, save='cancel')
        input_result = self.sj.linkage_get_input_condition_compound()
        self.assertEqual(input_result[0], '编辑输入条件(0)')
        self.sj.linkage_interface_choose_btn('left_click')
        # 再次选择主机，回路，地址号
        self.sj.linkage_edit_input_condition_compound(host=6, loop=3, device_addr=7, is_add=True, save='confirm')
        # 点击编辑输入条件后，选择取消
        self.sj.linkage_interface_choose_btn('left_click')
        self.sj.linkage_edit_input_condition_compound(save='cancel')
        # 判断输入条件是否仍为原来的状态
        input_result = self.sj.linkage_get_input_condition_compound()
        self.assertEqual(input_result[0], '编辑输入条件(1)')
        self.assertEqual(input_result[1][0], '6主机42回路板83回路7号')
        # 还原测试环境
        self.sj.linkage_interface_choose_btn('back_btn')


if __name__ == "__main__":
    unittest.main(verbosity=2)
    # run_suite(TestLinkage)
