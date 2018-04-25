"""
    联动设置相关页面封装
"""
from libs.app import Controller
from libs.log import *
from time import sleep


class Getoutofloop(Exception):
    pass


class Linkage(Controller):
    # 联动原则id
    build_id = ['acoustooptic', 'broadcast', 'elevator_crash', 'cut_electric', 'air_fan', 'emergency_lighting']
    neighbor_floor_id = ['air_valve']
    self_floor_id = ['floor_broadcast']
    principle_ids = build_id + neighbor_floor_id + self_floor_id

    def linkage_list_btn(self, linkage_id=None, list_value=None):
        """
        点击界面元素： 返回，统计，筛选，添加，全部生效，全部失效，全部删除，广播与声光交替
        界面:联动列表
        :param linkage_id: back, statistics, filter, add, effective, dis_effective, delete, broadcast_and_toec
        :param list_value: 联动列表中元素[序号，输入条件]
        :return:
        """
        try:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_programme_%s_btn' % linkage_id).click()
            self.clog(get_current_info() + 'Click %s in linkage setting.' % linkage_id)
        except:
            if list_value:
                list_num = list_value[0]
                list_input = list_value[1]
                ele_list_input = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_%s' % list_input)
                ele_input_text = [ele_list_input[i].get_attribute('text') for i in range(len(ele_list_input))]
                input_text = ele_input_text[list_num-1]
                ele_list_input[list_num-1].click()
                self.clog(get_current_info() + "Click number %s ->>> %s in linkage list" % (list_num, input_text))

    def linkage_list_btn_confirm(self, is_confirm=True):
        """
        点击确定还是返回
        界面：联动列表界面扩展界面
        :param is_confirm: bool，确定还是返回
        :return:
        """
        if is_confirm:
            self.driver.find_element_by_name('确定').click()
            sleep(1)
        else:
            self.driver.find_element_by_name('返回').click()

    def linkage_add(self, index):
        """
        按索引选择联动类型，如0代表联动原则，1代表系统原则，index最大为12
        界面：添加联动
        :param index: 联动类型的索引值
        :return:
        """
        elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/dialog_product_type_name')
        ele_name = elements[index].get_attribute('text')
        elements[index].click()
        self.clog(get_current_info() + "Enter %s Surface in linkage_add" % ele_name)

    def linkage_principle_choose(self, index=0, is_choose_all=False, is_check=False, is_make=False):
        """
        联动原则选择界面1相关操作
        栋：声光警报器,广播,电梯迫降,切断市电, 正压风机, 应急照明,
        ('acoustooptic', 'broadcast', 'elevator_crash', 'cut_electric', 'air_fan', 'emergency_lighting')
        本层或邻层：正压风阀air_valve
        本层: 声光报警器-广播floor_broadcast
        （通过checked的值是true还是false来区分是否被选中）
        界面：联动原则选择（界面1）
        :index: principle_ids的索引位置，从0开始，分别对应相应的principle_id
        :is_choose_all: 是否全选。若为True，则忽略其他所有的参数
        :is_check: 检查该索引对应的联动是否被选中. （不支持全选时检查，只能单个单个检查）
        :is_make: 是否生成联动原则
        :return:若is_check为True则返回是否被选中的结果
        """
        if not is_choose_all:
            if index == 7 or index == -1:
                # 声光报警器-广播 这项本层联动需要下拉才能选中
                x, y = Controller.app_get_size(self)
                self.driver.swipe(start_x=x * 0.75, start_y=y * 0.78, end_x=x * 0.75, end_y=y * 0.4, duration=500)
                sleep(2)
                ele = self.driver.find_element_by_id(
                    'com.fhsj.jbqbl.launcher:id/linkage_principle_%s_select' % self.principle_ids[index])
                raw_checked_value = ele.get_attribute('checked')
                # 该控件点击经常无反应，尝试多次点击解决
                for num in range(5):
                    ele.click()
                    sleep(1)
                    ele = self.driver.find_element_by_id(
                        'com.fhsj.jbqbl.launcher:id/linkage_principle_%s_select' % self.principle_ids[index])
                    aim_check_value = ele.get_attribute('checked')
                    if raw_checked_value != aim_check_value:
                        break

            else:
                # 选择联动原则
                ele = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_%s_select'% self.principle_ids[index])
                ele.click()
                checked_value = ele.get_attribute('checked')
                self.clog(get_current_info() + '%s is selected or not: %s' % (self.principle_ids[index], checked_value))
        else:
            for i in range(8):
                self.linkage_principle_choose(index=i, is_choose_all=False)
        # 检查
        if is_check and not is_choose_all:
            checked = ele.get_attribute('checked')
            return True if checked == 'true' else False
        # 生成联动
        if is_make:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_make_btn').click()

    def linkage_principle_choose_btn(self, btn):
        """
        点击按钮。
        界面：联动原则选择界面1(返回，生成联动）、联动原则选择界面2（返回，上一步，保存）、联动条目预览（返回）
        :param btn: back, make, previous, save,
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_%s_btn'%btn).click()
        self.clog(get_current_info() + "Click %s in 联动原则界面" % btn)

    def linkage_principle_make_get_count(self, area, is_preview=False):
        """
        预览 或者 获取栋，邻层，本层联动原则推荐数和已选择数。
        界面：联动原则选择界面2
        :param area: 0表示栋联动，1表示邻层联动， 2表示本层联动
        :param is_preview: 是否预览相应联动信息，True则点击预览进入预览界面
        :return:返回元祖，（推荐数，选择数) (int(recommend_count), int(select_count))
        """

        if area == 0:
            # 栋联动推荐数
            recommend_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_building_recommend_count').get_attribute('text')
            # 栋联动已选择数
            select_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_building_select_count').get_attribute('text')
            if is_preview:
                # 预览
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_building_preview_btn').click()
            return (int(recommend_count), int(select_count))
        if area == 1:
            # 邻层联动推荐数
            recommend_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_adjacent_recommend_count').get_attribute('text')
            # 邻层联动已选择数
            select_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_adjacent_select_count').get_attribute('text')
            # 邻层联动预览
            if is_preview:
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_adjacent_preview_btn').click()
            return (int(recommend_count), int(select_count))
        # # 本层联动信息需要下拉才能查看
        if area == 2:
            x, y = Controller.app_get_size(self)
            self.driver.swipe(start_x=x * 0.75, start_y=y * 0.78, end_x=x * 0.75, end_y=y * 0.4, duration=500)
            sleep(2)
            recommend_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_floor_recommend_count').get_attribute('text')
            select_count = self.driver.find_element_by_id(
                'com.fhsj.jbqbl.launcher:id/linkage_principle_floor_select_count').get_attribute('text')
            if is_preview:
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_floor_preview_btn').click()
            return (int(recommend_count), int(select_count))

    def linkage_list_reg(self):
        """
        获取当前页面中联动数和当前页面生效联动数
        界面：联动列表
        :return: tuple
        """
        ele_regs = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_register')
        regs_value = [ele.get_attribute('checked') for ele in ele_regs]
        # 当前页面联动数
        count = len(ele_regs)
        # 当前页面生效联动数
        count_eff =regs_value.count('true')
        return (count, count_eff)

    def linkage_get_list_count(self):
        """
        获取联动列表中联动总数
        界面：联动列表
        :return: int联动总数
        """
        count = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_programme_list_count').get_attribute('text')
        return int(count)

    def linkage_get_list_information(self):
        """
        获取联动列表上的信息，包括序号、联动类型、联动范围、输入条件、输出结果
        界面：联动列表界面
        :return: result[]
        """
        result = []
        ele_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_num')
        num_text = [ele_num[i].get_attribute('text') for i in range(len(ele_num))]
        result.append(num_text)
        ele_type = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_type')
        type_text = [ele_type[i].get_attribute('text') for i in range(len(ele_type))]
        result.append(type_text)
        ele_range = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_range')
        range_text = [ele_range[i].get_attribute('text') for i in range(len(ele_range))]
        result.append(range_text)
        ele_input = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_input')
        input_text = [ele_input[i].get_attribute('text') for i in range(len(ele_input))]
        result.append(input_text)
        ele_output = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_list_output')
        output_text = [ele_output[i].get_attribute('text') for i in range(len(ele_output))]
        result.append(output_text)
        self.clog(get_current_info() + "Get information in linkage list.")
        return result

    def linkage_principle_preview(self, is_select_all=False, is_select_none=False):
        """
        获取当前页面联动总数和已选择联动数
        界面：联动条目预览
        :param is_select_all: 是否点击全选
        :param is_select_none: 是否点击取消选择
        :return:
        """
        if is_select_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_preview_select_all').click()
        if is_select_none:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_preview_select_none').click()
        # 联动总数
        ele_regs = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_preview_register')
        regs_value = [ele.get_attribute('checked') for ele in ele_regs]
        count = len(ele_regs)
        # 已选择数
        count_select = regs_value.count('true')
        return (count, count_select)

    def linkage_principle_preview_get_status(self, index, is_click):
        """
        获取联动原则是否注册的状态
        界面：联动条目预览
        :index: 索引号，0开始
        :is_click: bool是否点击该联动原则
        :return: bool 注册状态
        """
        ele_regs = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/linkage_principle_preview_register')
        if is_click:
            ele_regs[index].click()
        value = ele_regs[index].get_attribute('checked')
        return True if value == 'true' else False

    def linkage_edit_input_condition(self, index=None, condition=None, save=None, del_num=None, is_del_all=False):
        """
        界面：编辑输入条件
        :param index:  按照索引值选择xxx联动的输入条件，下标范围是[0~11]，如0代表光电探测器，1代表感温探测器
        :param condition: 条件相与 或 条件相或
        :param save: 是否保存
        :param del_num: 单个删除已选择项
        :param is_del_all:  全部删除
        :return:
        """
        # 选择输入条件
        if index:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/dialog_device_type_name')
            for i in range(len(index)):
                ele_device_name = elements[index[i]].get_attribute('text')
                elements[index[i]].click()
                self.clog(get_current_info() + "Select input device type: %s" % ele_device_name)
        # 条件相与 或者 条件相或
        if condition:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/condition_%s' % condition).click()
            self.clog(get_current_info() + "Click condition is %s" % condition)
        # 单个删除已选择项
        if del_num:
            ele_deleted = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/delete')
            for i in range(len(del_num)):
                del_device_type = ele_deleted[del_num[i]].get_attribute('text')
                ele_deleted[del_num[i]].click()
                self.clog(get_current_info() + "Delete input device type : %s" % del_device_type)
        # 全部删除已选择项
        if is_del_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delete_all').click()
            self.clog(get_current_info() + "Delete all input device type")
        # 获取已选择项的设备类型
        try:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_name')
            list_selected_item = [elements[i].get_attribute('text') for i in range(len(elements))]
        except:
            list_selected_item = None
        # 是否保存
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % save).click()
            self.clog(get_current_info() + "In edit input condition interface, click %s" % save)
        return list_selected_item

    def linkage_edit_input_condition_compound(self, host=None, loop=None, device_addr=None, is_add=False, del_num=None, is_del_all=False, save=None):
        """
        界面：复合联动 ->>> 选择输入条件
        :param host: 主机
        :param loop: 回路
        :param device_addr: 设备地址号
        :param is_add: 是否添加到输入条件
        :param del_num: 单个删除
        :param is_del_all: 全部删除
        :param save: 是否保存
        :return: 已选择项的设备 list_selected_item
        """
        if host:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/host_spinner').click()
            # 将数字回归至最初状态
            self.app_swipe_loops(start_x=312, start_y=404, end_x=312, end_y=638, times=35)
            ele_host = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if host <= 7:
                ele_host[host - 1].click()
            else:
                try:
                    for i in range(37):
                        self.driver.swipe(start_x=312, start_y=638, end_x=312, end_y=404, duration=900)
                        ele_host = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_host[j].get_attribute('text') for j in range(len(ele_host))]
                        for k in range(len(ele_host)):
                            if ele_text[k] == str(host):
                                ele_host[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the host is : %s" % host)
        if loop:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/loop_spinner').click()
            # 将数字回归至最初状态
            self.app_swipe_loops(start_x=508, start_y=404, end_x=508, end_y=638, times=12)
            ele_loop = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if loop <= 7:
                ele_loop[loop - 1].click()
            else:
                try:
                    for i in range(12):
                        self.driver.swipe(start_x=508, start_y=638, end_x=508, end_y=404, duration=900)
                        ele_loop = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_loop[j].get_attribute('text') for j in range(len(ele_loop))]
                        for k in range(len(ele_loop)):
                            if ele_text[k] == str(loop):
                                ele_loop[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the loop is : %s" % loop)
        if device_addr:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/device_addr_spinner').click()
            # 将数字回归至最初状态
            self.app_swipe_loops(start_x=704, start_y=404, end_x=704, end_y=638, times=48)
            ele_device_addr = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if device_addr <= 7:
                ele_device_addr[device_addr - 1].click()
            else:
                try:
                    for i in range(48):
                        self.driver.swipe(start_x=704, start_y=638, end_x=704, end_y=404, duration=900)
                        ele_device_addr = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_device_addr[j].get_attribute('text') for j in range(len(ele_device_addr))]
                        for k in range(len(ele_device_addr)):
                            if ele_text[k] == str(device_addr):
                                ele_device_addr[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the device_address is : %s" % device_addr)
        if is_add:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/add').click()
            self.clog(get_current_info() + "Add to input condition.")
        if del_num:
            ele_deleted = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/delete')
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_device_addr')
            for i in range(len(del_num)):
                del_device = elements[del_num[i]].get_attribute('text')
                ele_deleted[del_num[i]].click()
                self.clog(get_current_info() + "Delete input device address : %s." % del_device)
        if is_del_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delete_all').click()
            self.clog(get_current_info() + "Delete all input device address")
        # 获取已选择项的设备
        try:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_device_addr')
            list_selected_item = [elements[i].get_attribute('text') for i in range(len(elements))]
        except:
            list_selected_item = None
        # 是否保存
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % save).click()
            self.clog(get_current_info() + "Click %s" % save)
        return list_selected_item

    def linkage_edit_output_result(self, device_type=None, loop=None, community=None, building=None, floor=None,
                                   is_clear_filter=False, index=None, is_select_all=None, save=None, del_num=None,
                                   is_del_all=False):
        """
        界面：xxx联动 ->>> 选择输出结果界面
        :param device_type: 设备类型
        :param loop: 回路
        :param community: 区
        :param building: 栋
        :param floor: 层
        :param is_clear_filter: 清除筛选条件
        :param index: 根据调试码的下标点击设备，下标范围是[0~6]
        :param is_select_all: 全选
        :param save: 是否保存
        :param del_num: 单个删除设备，以列表形式传参，del_num下标范围[0~8]
        :param is_del_all:  全部删除
        :return: 返回列表 [[设备类型],[位置],[调试码]]
        """
        if device_type:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/devicetype_spinner').click()
            try:
                # elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                # elements[device_type].click()  # 按照下标来点击
                self.driver.find_element_by_name(device_type).click()
                self.clog(get_current_info() + "Select device type is %s" % device_type)
            except:
                pass
        if loop:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/loop_spinner').click()
            try:
                # elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                # elements[loop].click()  # 按照下标来点击
                self.driver.find_element_by_name(loop).click()
                self.clog(get_current_info() + "Select loop is %s" % loop)
            except:
                pass
        if community:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/comm_spinner').click()
            try:
                # elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                # elements[community].click()  # 按照下标来点击
                self.driver.find_element_by_name(community).click()
                self.clog(get_current_info() + "Select community is %s" % community)
            except:
                pass
        if building:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/building_spinner').click()
            try:
                # elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                # elements[building].click()  # 按照下标来点击
                self.driver.find_element_by_name(building).click()
                self.clog(get_current_info() + "Select building is %s" % building)
            except:
                pass
        if floor:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/floor_spinner').click()
            try:
                # elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                # elements[floor].click()  # 按照下标来点击
                self.driver.find_element_by_name(floor).click()
                self.clog(get_current_info() + "Select floor is %s" % floor)
            except:
                pass
        if is_clear_filter:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delete_filter').click()
            self.clog(get_current_info() + "Clear filter in edit output interface")
        if index:
            ele_index = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/debug_code')
            for i in range(len(index)):
                ele_index[index[i]].click()
        if is_select_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/output_choice_selectall').click()
            self.clog(get_current_info() + "Select all device")
        if del_num:
            ele_del = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/delete')
            device_type = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/devicetype')
            for i in range(len(del_num)):
                value = device_type[del_num[i]].get_attribute('text')
                ele_del[del_num[i]].click()
                self.clog(get_current_info() + "Delete device type %s" % value)
        if is_del_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delete_all').click()
            self.clog(get_current_info() + "Delete all device type")
        try:
            result = []
            ele_debug_code = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/debug_code')
            ele_device_type = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/devicetype')
            ele_location = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location')
            list_debug_code = [ele_debug_code[i].get_attribute('text') for i in range(len(ele_debug_code))]
            list_device_type = [ele_device_type[i].get_attribute('text') for i in range(len(ele_device_type))]
            list_location = [ele_location[i].get_attribute('text') for i in range(len(ele_location))]
            result.append(list_device_type)
            result.append(list_location)
            result.append(list_debug_code)
            self.clog(get_current_info() + "Get device_type/location/debug_code")
        except:
            result = None
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % save).click()
            self.clog(get_current_info() + "In edit output result interface, click %s" % save)
        return result

    def linkage_edit_output_result_layer(self, index=None, save=None, del_num=None, is_del_all=False):
        """
        界面：层中联动 ->>> 选择结果输出
        :param index: 按照索引值选择xxx联动的输出结果，下标范围是[0~11]，如0代表声光报警器，1代表广播
        :param save: 是否保存
        :param del_num: 单个删除已选择项
        :param is_del_all: 全部删除
        :return: list[已选择项]
        """
        # 选择输出结果
        if index:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/dialog_device_type_name')
            for i in range(len(index)):
                ele_device_name = elements[index[i]].get_attribute('text')
                elements[index[i]].click()
                self.clog(get_current_info() + "Select output device type: %s" % ele_device_name)
        # 单个删除已选择项
        if del_num:
            ele_deleted = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/delete')
            for i in range(len(del_num)):
                del_device_type = ele_deleted[del_num[i]].get_attribute('text')
                ele_deleted[del_num[i]].click()
                self.clog(get_current_info() + "Delete output device type : %s" % del_device_type)
        # 全部删除已选择项
        if is_del_all:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delete_all').click()
            self.clog(get_current_info() + "Delete all output device type")
        # 获取已选择项的设备类型
        try:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_name')
            list_selected_item = [elements[i].get_attribute('text') for i in range(len(elements))]
        except:
            list_selected_item = None
        # 是否保存
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % save).click()
            self.clog(get_current_info() + "In edit input condition interface, click %s" % save)
        return list_selected_item

    def linkage_get_input_condition(self):
        """
        界面：(系统、区中、栋中、层中、房中)联动界面
        包括：编辑输入条件，编辑输出条件，输入范围，输出延时等等界面信息
        :return: list
        """
        input_result = []

        # 编辑输入条件
        input_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/edit_input').get_attribute('text'))
        # 条件：相或/相与
        input_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/condition').get_attribute('text'))
        # 输入文本框 --- 选项内容
        ele_input_name = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_name')
        input_name = [ele_input_name[i].get_attribute('text') for i in range(len(ele_input_name))]
        input_result.append(input_name)
        # 输入范围
        try:
            input_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/input_range').get_attribute('text'))
        except:
            pass
        # 至少报警个数
        try:
            input_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/limit_alarm_spinner').get_attribute('text'))
        except:
            pass
        self.clog(get_current_info() + "Get linkage input condition information")
        return input_result

    def linkage_get_input_condition_compound(self):
        list_selected_result = []
        # 编辑输入条件
        list_selected_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/edit_input').get_attribute('text'))
        # 已选择项
        ele_device_addr = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/input_device_addr')
        device_addr = [ele_device_addr[i].get_attribute('text') for i in range(len(ele_device_addr))]
        list_selected_result.append(device_addr)
        return list_selected_result
        
    def linkage_get_output_result(self):
        """
        界面：xxx联动界面
        包括：编辑输出结果，输出延时等等界面信息
        :return: list ->>> output_result[8]
        """
        output_result = []
        # 0、编辑输出结果
        output_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/edit_output').get_attribute('text'))
        # 1、输出延时
        output_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/delay_spinner').get_attribute('text'))
        # 2、生效
        output_result.append(
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/effect').get_attribute('checked'))
        try:
            # 3、输出结果文本框 --- 设备类型
            ele_device_name = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/devicename')
            device_name = [ele_device_name[i].get_attribute('text') for i in range(len(ele_device_name))]
            output_result.append(device_name)
            # 4、输出结果文本框 --- 位置  （层中联动没有这一项）
            ele_location = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/location')
            location = [ele_location[i].get_attribute('text') for i in range(len(ele_location))]
            output_result.append(location)
            # 5、输出结果文本框 --- 调试码  （层中联动没有这一项）
            ele_debug_code = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/debug_code')
            debug_code = [ele_debug_code[i].get_attribute('text') for i in range(len(ele_debug_code))]
            output_result.append(debug_code)
        except:
            pass
        # 6、输入与输出范围   （只在层中联动中）
        try:
            output_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/input_output_range').get_attribute('text'))
        except:
            pass
        # 7、是否启动邻层   （只在层中联动（类型输出）中）
        try:
            output_result.append(self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/adjacent_effect').get_attribute('checked'))
        except:
            pass
        self.clog(get_current_info() + "Get linkage output condition information")
        return output_result

    def linkage_interface_choose_btn(self, button=None, limit_alarm=None, delay=None, is_effective=None,
                                     is_adjacent=False, save=None):
        """
        点击按钮
        界面：xxx联动结果展示界面
        :param button: 编辑输入条件，编辑输出条件，保存，保存并继续添加，返回，生效，输入范围的更改  等等
        :param limit_alarm: 至少报警个数
        :param delay: 输出延时
        :param is_effective: 是否生效
        :param save: 是否保存 或 是否保存并继续添加
        :return:
        """
        if button:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % button).click()
            self.clog(get_current_info() + "Choose click %s button" % button)
        if limit_alarm:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            elements[limit_alarm-1].click()
            self.clog(get_current_info() + "Choose the number of limit_alarm")
        if delay:
            elements = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            elements[delay-1].click()
            self.clog(get_current_info() + "Choose output delay")
        if is_effective:
            ele_effective = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/effect')
            ele_effective.click()
            effect = ele_effective.get_attribute('checked')
            self.clog(get_current_info() + "Make this linkage into effect: not %s" % effect)
        if is_adjacent:
            ele_adjacent = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/adjacent_effect')
            ele_adjacent.click()
            effect = ele_adjacent.get_attribute('checked')
            self.clog(get_current_info() + "Make adjacent layer effect: %s" % effect)
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/%s' % save).click()
            self.clog(get_current_info() + "Choose click %s button" % save)

    def linkage_input_range_change(self, community=None, building=None, startfloor=None, endfloor=None,
                                   startroom=None, endroom=None, coordinate=None, save=None):
        """
        界面：选择范围
        :param community: 区
        :param building: 栋
        :param startfloor: 层
        :param endfloor: 层
        :param startroom: 房
        :param endroom: 房
        :param coordinate: 坐标，列表形式传参数 [[],[],[]]
        :param save: 是否保存
        :return:
        """
        if community:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_comm_spinner').click()
            ele_comm = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if community <= 7:
                ele_comm[community-1].click()
            else:
                try:
                    for i in range(16):
                        self.driver.swipe(start_x=coordinate[0][0], start_y=coordinate[0][1], end_x=coordinate[0][2], end_y=coordinate[0][3], duration=900)
                        ele_comm = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_comm[j].get_attribute('text') for j in range(len(ele_comm))]
                        for k in range(len(ele_comm)):
                            if ele_text[k] == str(community):
                                ele_comm[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the community is : %s" % community)
        if building:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_building_spinner').click()
            ele_build = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if building <= 7:
                ele_build[building-1].click()
            else:
                try:
                    for i in range(16):
                        self.driver.swipe(start_x=coordinate[1][0], start_y=coordinate[1][1], end_x=coordinate[1][2], end_y=coordinate[1][3], duration=900)
                        ele_build = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_build[j].get_attribute('text') for j in range(len(ele_build))]
                        for k in range(len(ele_build)):
                            if ele_text[k] == str(building):
                                ele_build[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the building is : %s" % building)
        if startfloor:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_startfloor_spinner').click()
            ele_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if startfloor <= -4:
                ele_floor[startfloor-1].click()
            else:
                try:
                    for i in range(30):
                        self.driver.swipe(start_x=coordinate[2][0], start_y=coordinate[2][1], end_x=coordinate[2][2], end_y=coordinate[2][3], duration=900)
                        ele_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_floor[j].get_attribute('text') for j in range(len(ele_floor))]
                        for k in range(len(ele_floor)):
                            if ele_text[k] == str(startfloor):
                                ele_floor[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the floor is : %s" % startfloor)
        if endfloor:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_endfloor_spinner').click()
            ele_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if endfloor <= -4:
                ele_floor[endfloor-1].click()
            else:
                try:
                    for i in range(30):
                        self.driver.swipe(start_x=coordinate[3][0], start_y=coordinate[3][1], end_x=coordinate[3][2], end_y=coordinate[3][3], duration=900)
                        ele_floor = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_floor[j].get_attribute('text') for j in range(len(ele_floor))]
                        for k in range(len(ele_floor)):
                            if ele_text[k] == str(endfloor):
                                ele_floor[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the floor is : %s" % endfloor)
        if startroom:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_startroom_spinner').click()
            ele_room = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if startroom <= 7:
                ele_room[startroom-1].click()
            else:
                try:
                    for i in range(37):
                        self.driver.swipe(start_x=coordinate[3][0], start_y=coordinate[3][1], end_x=coordinate[3][2], end_y=coordinate[3][3], duration=900)
                        ele_room = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_room[j].get_attribute('text') for j in range(len(ele_room))]
                        for k in range(len(ele_room)):
                            if ele_text[k] == str(startroom):
                                ele_room[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the startroom is : %s" % startroom)
        if endroom:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_endroom_spinner').click()
            ele_room = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
            if endroom <= 7:
                ele_room[endroom-1].click()
            else:
                try:
                    for i in range(37):
                        self.driver.swipe(start_x=coordinate[4][0], start_y=coordinate[4][1], end_x=coordinate[4][2], end_y=coordinate[4][3], duration=900)
                        ele_room = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')
                        ele_text = [ele_room[j].get_attribute('text') for j in range(len(ele_room))]
                        for k in range(len(ele_room)):
                            if ele_text[k] == str(endroom):
                                ele_room[k].click()
                                raise Getoutofloop()  # 使用自定义异常，跳出多重for循环
                except Getoutofloop:
                    pass
            self.clog(get_current_info() + "Choose the endroom is : %s" % endroom)
        if save:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_linkage_input_range_%s' % save).click()
            self.clog(get_current_info() + "Click %s in input range interface " % save)




