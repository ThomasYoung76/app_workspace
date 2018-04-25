"""
    防火分区
"""
from libs import *


class Fire_Compartment(Controller):

    def fire_compartment_btn(self, compartment_id):
        """
        点击界面元素：返回，添加，生效，删除
        界面：防火分区
        :param compartment_id: back, add, effective_tx, delete_tx
        :return:
        """
        try:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_%s_btn'%compartment_id).click()
            self.clog(get_current_info() + 'Click %s in fire compartment surface' % compartment_id)
        except:
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_%s' % compartment_id).click()
            self.clog(get_current_info() + 'Click %s option' % compartment_id)

    def fire_compartment_dialog(self, back_save_id):
        """
        点击界面元素：生效/删除
        界面：防火分区-生效/删除提示框
        :param back_save_id:
        :return:
        """
        self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/dialog_back_save_%s' % back_save_id).click()
        self.clog(get_current_info() + 'Click %s in tip dialog' % back_save_id)

    def fire_compartment_get_order(self, comp_num):
        """
        防火分区列表，获取生效信息，包括是否生效
        界面：防火分区界面
        :param comp_num:序号
        :return:
        """
        result = {}
        if comp_num:
            # 获取生效信息
            ele_reg_comp = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_register')
            # 序号控件集
            ele_comp_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_num')
            list_comp_num = [ele_comp_num[i].get_attribute('text') for i in range(len(ele_comp_num))]
            comp_index = list_comp_num.index(str(comp_num))  # 找出comp_num的索引位置
            is_order = ele_reg_comp[comp_index].get_attribute('checked')  # is_order 给出来的是当前复选框是否生效的状态
            result['is_order'] = is_order
            result['comp_index'] = comp_index
            return result

    def fire_compartment_order(self, comp_num, is_action=True):
        """是否生效"""
        result = self.fire_compartment_get_order(comp_num)
        if is_action:
            ele_comp_order = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_register')
            if result.get('is_order'):
                ele_comp_order[result.get('comp_index')].click()
            else:
                ele_comp_order[result.get('comp_index')].click()
        return result

    def fire_compartment_add(self, comp_locate=None, comp_build=None, comp_floor1=None, comp_floor2=None, comp_room=None,
                             is_batch=False, comp_decs=None, is_effective=False, is_save=True):
        """
        添加防火分区信息
        界面：防火分区添加界面
        :param comp_locate: 选择区号
        :param comp_build: 选择栋号
        :param comp_floor1: 选择层1
        :param comp_floor2: 选择层2
        :param comp_room: 选择房号
        :param is_batch: 是否批量选择房号
        :param comp_decs: 填写位置信息
        :param is_effective: 是否生效
        :param is_save: 是否保存
        :return:
        """
        if comp_locate:
            self.clog(get_current_info() + "Choose compartment %s community" % comp_locate)
            index = comp_locate % 7
            if index == 0:
                index = 6
            else:
                index = index - 1
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_com_spinner').click()
            if comp_locate == index + 1:
                self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[index].click()
            else:
                for i in range(16):
                    # 对应坐标：comp_locate[0]->>>(112,238), comp_locate[5]->>>(112,433), comp_locate[6]->>>(112,472)
                    self.app_swipe_loops(start_x=112, start_y=472, end_x=112, end_y=238, times=1)
                    if comp_locate == 7 * i + index + 1:
                        self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[index].click()
                        break
                    else:
                        pass
        if comp_build:
            self.clog(get_current_info() + "Choose compartment %s build" % comp_build)
            index = comp_build % 7
            if index == 0:
                index = 6
            else:
                index = index - 1
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_buil_spinner').click()
            if comp_build == index + 1:
                self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[index].click()
            else:
                for i in range(16):
                    self.app_swipe_loops(start_x=269, start_y=472, end_x=269, end_y=238, times=1)
                    if comp_build == 7 * i + index + 1:
                        self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[index].click()
                        break
                    else:
                        pass
        if comp_floor1:
            self.clog(get_current_info() + "Choose compartment %s floor"% comp_floor1)
            # 后期需要完善下拉,选择层的功能
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_floor_spinner1').click()
            self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[comp_floor1].click()
        if comp_floor2:
            self.clog(get_current_info() + "Choose compartment %s floor"% comp_floor2)
            # 后期需要完善下拉,选择层的功能
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_floor_spinner2').click()
            self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/data_text')[comp_floor2].click()
        if is_batch:
            self.clog(get_current_info() + "Batch choosing rooms")
            list_room = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_gird_item_room_tx')
            if comp_room[0] > 132:
                self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_grid_view_second_page').click()
                for i in range(comp_room[0]-133, comp_room[1]+1):
                    list_room[i-1].click()
            else:
                for i in range(comp_room[0], comp_room[1]+1):
                    list_room[i-1].click()
        else:
            if comp_room:
                self.clog(get_current_info() + "Choosing %s room " % comp_room)
                if comp_room > 132:
                    self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_grid_view_second_page').click()
                    self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_gird_item_room_tx')[comp_room - 133].click()
                else:
                    self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_gird_item_room_tx')[comp_room - 1].click()
        if comp_decs:
            self.clog(get_current_info() + "Add fire compartment locate description")
            ele_decs = self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_description_et')
            ele_decs.click()
            ele_decs.clear()
            ele_decs.send_keys(comp_decs)
            self.driver.hide_keyboard()
        if is_effective:
            self.clog(get_current_info() + "Make this fire compartment not effective: %s" % is_effective)
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_register_cb').click()
        if is_save:
            self.clog(get_current_info() + "Save this fire compartment: %s" % is_save)
            self.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_select_save').click()

    def fire_compartment_get_info(self, number):
        """
        获取防火分区界面上的其中一条信息
        界面：防火分区列表界面
        result['block_layer']：区栋层
        result['rooms']：房
        result['location']：位置
        result['effective']：生效
        :return: dict() ->>> result{}
        """
        # 获取区栋层的信息
        self.clog(get_current_info() + "Get fire compartment information from list")
        result = dict()
        # 获取区栋层的信息
        ele_block_layer = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_location')
        list_block_layer = [ele_block_layer[i].get_attribute('text') for i in range(len(ele_block_layer))]
        block_layer = list_block_layer[number-1]
        result['block_layer'] = block_layer

        # 获取房的信息
        ele_rooms = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_room')
        list_rooms = [ele_rooms[i].get_attribute('text') for i in range(len(ele_rooms))]
        room = list_rooms[number-1]
        result['room'] = room

        # 获取位置的信息
        ele_location = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_location_desc')
        list_location = [ele_location[i].get_attribute('text') for i in range(len(ele_location))]
        location = list_location[number-1]
        result['location'] = location

        # 获取生效状态
        ele_effective = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_register')
        list_effective = [ele_effective[i].get_attribute('checked') for i in range(len(ele_effective))]
        effective = list_effective[number-1]
        result['effective'] = effective
        return result

    def fire_compartment_get_last_number(self):
        """
        获取防火分区列表最后一条内容的序号
        界面：防火分区列表界面
        :return: number
        """
        try:
            ele_num = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_num')
            list_num = [ele_num[i].get_attribute('text') for i in range(len(ele_num))]
            number = list_num[-1]
        except:
            number = None
        return number

    def fire_compartment_delete(self, comp_num):
        """
        获取删除按钮
        界面：防火分区列表界面
        :param comp_num: 序号
        :return: delete_btn
        """
        self.clog(get_current_info() + "Get delete button in fire compartment list")
        ele_delete_btn = self.driver.find_elements_by_id('com.fhsj.jbqbl.launcher:id/fire_compartment_list_delete')
        delete_btn = ele_delete_btn[comp_num-1]
        return delete_btn
