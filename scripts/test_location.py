"""
    联动设置-区栋层
"""
import sys
sys.path.append('..')
from libs import *
import unittest


class Location(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sj = Controller()

    def setUp(self):
        self.sj.driver.implicitly_wait(5)
        pass

    def tearDown(self):
        self.sj.driver.implicitly_wait(2)
        flag = self.sj.app_back_main_page()
        if not flag:
            try:
                self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_back_btn').click()
                flag = self.sj.app_is_main_page()
            except:
                pass
        if not flag:
            try:
                self.sj.driver.find_element_by_id("com.fhsj.jbqbl.launcher:id/menu_back_btn").click()
                self.sj.app_is_main_page()
            except:
                pass

    def test_location_168(self):
        """没登记区时，不可登记栋，没登记栋时，不可登记层"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 不登记区
        result = self.sj.app_location(comm_num=1, is_register=(False, False, False))
        # 区的扩展图标不可被选中
        self.assertFalse(result.get('comm_icon'))
        # 登记区、不登记栋
        result = self.sj.app_location(comm_num=1, build_num=2, is_register=(True, False, False))
        try:
            # 栋的扩展图标不可被选中
            self.assertFalse(result.get('build_icon'))
        finally:
            # 取消登记区
            self.sj.app_location(comm_num=1, is_register=(False,), is_save=True)

    def test_location_166_0(self):
        """单个注册、去注册区、栋、层。去注册区，则栋信息可以隐藏"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 单个登记区栋层、并输入相应位置信息
        args_location = {'comm_num': 2, 'comm_locate': '123a b_ddd', 'build_num': 1, 'build_locate': '9',
                         'floor_num': -1, 'is_register': (True, True, True)}
        result = self.sj.app_location(is_save=True, **args_location)
        try:
            # 检查单个区栋层均被注册
            self.assertTrue(result.get('is_comm_reg') and result.get('is_build_reg') and result.get('is_floor_reg'))
        finally:
            self.sj.app_menu(menu_id='location', is_click_menu=False)
            # 取消登记区，栋信息可以隐藏(result['comm_icon']=False)
            result = self.sj.app_location(comm_num=2, build_num=1, floor_num=-1,
                                          is_register=(False, True, True), is_save=True)
            # 检查栋信息被隐藏
            self.assertEqual(result.get('comm_icon'), False)

    def test_location_166_1(self):
        """单个注册，位置信息：长度，特殊字符，空，中英文，大小写，空格, 返回保存，返回不保存"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 单个登记区栋层、并输入相应位置信息
        comm, build, floor = 2, 8, 2
        args_location = {'comm_num': comm, 'comm_locate': '000333111', 'build_num': build,
                         'build_locate': '333000222', 'floor_num': floor, 'is_register': (True, True, True)}
        result = self.sj.app_location(is_save=True, **args_location)
        try:
            # 检查单个区栋层均被注册
            self.assertTrue(result.get('is_comm_reg') and result.get('is_build_reg') and result.get('is_floor_reg'))
            # 检查区、栋位置信息正确
            self.assertEqual(result.get('comm_loc'), args_location['comm_locate'])
            self.assertEqual(result.get('build_loc'), args_location['build_locate'])
        finally:
            self.sj.app_menu(menu_id='location', is_click_menu=False)
            # 取消登记区
            result = self.sj.app_location(comm_num=comm, is_register=(False,))
            # 检查栋信息被隐藏(result['comm_icon']=False)
            self.assertEqual(result.get('comm_icon'), False)
        # 未保存直接点击返回会出现保存的提示
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_back_btn').click()
        self.sj.app_is_display('设置已经修改，是否保存？')
        # 点击不保存，重新进入区栋层，区仍然是已注册状态
        self.sj.driver.find_element_by_name('不保存').click()
        self.sj.app_menu(menu_id='location', is_click_menu=False)
        result = self.sj.app_get_location(comm_num=comm)
        self.assertTrue(result.get('is_comm_reg'))
        # 修改区位置(区位置输入超过12个字符)
        comm_locate = 'abcdef123456yd'
        result = self.sj.app_location(comm_num=comm, comm_locate=comm_locate, is_register=(True, False, False))
        self.assertTrue(result.get('comm_loc'), comm_locate[:12])
        # 取消区登记
        self.sj.app_location(comm_num=comm, is_register=(False,))
        # 点击返回并保存
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_back_btn').click()
        self.sj.app_is_display('设置已经修改，是否保存？')
        self.sj.driver.find_element_by_name('保存').click()
        # 再进去区栋层，查看保存成功
        self.sj.app_menu(menu_id='location', is_click_menu=False)
        result = self.sj.app_get_location(comm_num=comm)
        self.assertEqual(result.get('comm_loc'), comm_locate[:12])

    def test_location_167_0(self):
        """批量区注册、去注册"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 批量注册1到3号区
        self.sj.app_location_batch_register('区注册', tap_loc=(1040, 620))
        # 检查1到3号被注册，其他号未被注册
        for i in range(4):
            ret = self.sj.app_get_location(comm_num=i + 1)
            if i == 3:
                self.assertFalse(ret.get('is_comm_reg'))
                break
            self.assertTrue(ret.get('is_comm_reg'))
        # 1号区去注册，但不提交
        self.sj.app_location_batch_register('区注册', is_register=False, is_submit=False)
        # 检查1号区仍处于注册状态
        ret = self.sj.app_get_location(comm_num=1)
        self.assertTrue(ret.get('is_comm_reg'))
        # 批量区注册1号区到3号区
        self.sj.app_location_batch_register('区注册', tap_loc=(1040, 620), is_register=False)
        # 检查1到3号区已去注册
        for i in range(3):
            ret = self.sj.app_get_location(comm_num=i + 1)
            self.assertFalse(ret.get('is_comm_reg'))
        # 保存操作
        self.sj.app_location(is_save=True)

    def test_location_167_1(self):
        """批量栋注册、层注册、去注册"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 注册1号区并展开栋信息
        self.sj.app_location(comm_num=1, is_register=(True,))
        # 批量注册1到3号栋
        self.sj.app_location_batch_register('栋注册', tap_loc=(1040, 620))
        # 检查1到3号栋被注册
        for i in range(3):
            ret = self.sj.app_get_location(comm_num=1, build_num=i + 1)
            self.assertTrue(ret.get('is_build_reg'))
        # 展开1区3栋的层信息
        self.sj.app_location(comm_num=1, build_num=3, is_register=(True, True))
        # 批量注册3栋的1到3层
        self.sj.app_location_batch_register('层注册', tap_loc=(1040, 620))
        # 检查1到3层被注册
        for i in range(3):
            ret = self.sj.app_get_location(comm_num=1, build_num=3, floor_num=i + 1)
            self.assertTrue(ret.get('is_floor_reg'))
        # 1号区去注册
        self.sj.app_location_batch_register('区注册', is_register=False)
        # 保存
        self.sj.app_location(is_save=True)

    def test_location_167_2(self):
        """批量区位置设置"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        # 注册1号区并展开栋信息
        self.sj.app_location(comm_num=1, is_register=(True,))
        # 注册1到3号区
        self.sj.app_location_batch_register_desc('区位置', tap_loc=(880, 620), location='abc987654')
        # 注册1到3号栋
        self.sj.app_location_batch_register_desc('栋位置', tap_loc=(880, 620), location='abcdef12345')
        # 检查区位置信息
        for i in range(1, 4):
            result = self.sj.app_get_location(comm_num=i)
            self.assertEqual(result['comm_loc'], 'abc987654')
        for i in range(1, 4):
            result = self.sj.app_get_location(comm_num=1, build_num=i)
            self.assertEqual(result['build_loc'], 'abcdef12345')
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_back_btn').click()
        self.sj.driver.find_element_by_name('不保存').click()

    def test_location_176(self):
        """可设置99个区99栋-10层至200层"""
        self.sj.app_login(user_num=user_num, password=user_password)
        self.sj.app_menu(menu_id='location')
        sleep(2) # sleep之后，不会产生Error：An unknown server-side error occurred while processing the command
        # 重复从当页最后一行区号上滑到第一行（186，761）-> （186， 334），即可将区号下滑到最后一行
        self.sj.app_swipe_loops(start_x=186, start_y=761, end_x=186, end_y=334, times=16)
        result = self.sj.app_get_location(comm_num=99)
        self.assertEqual(result.get('list_comm_num')[-1], str(99))
        # 注册第99号区
        self.sj.app_location(comm_num=99)
        # 重复从当页最后一行栋号上滑到第一行（900，761）-> （900， 334），即可将栋号下滑到最后一行
        self.sj.app_swipe_loops(start_x=900, start_y=761, end_x=900, end_y=334, times=16)
        result = self.sj.app_get_location(build_num=99)
        self.assertEqual(result.get('list_build_num')[-1], str(99))
        # 注册第99层
        self.sj.app_location(build_num=99)
        # 层数滑到最上面-10层
        self.sj.app_swipe_loops(start_x=1550, start_y=334, end_x=1550, end_y=761, times=2)
        result = self.sj.app_get_location(floor_num=-10)
        self.assertEqual(result.get('list_floor_num')[0], str(-10))
        # 层数滑到最下面200层
        self.sj.app_swipe_loops(start_x=1550, start_y=761, end_x=1550, end_y=334, times=35)
        result = self.sj.app_get_location(floor_num=200)
        self.assertEqual(result.get('list_floor_num')[-1], str(200))
        # 注册第200层
        self.sj.app_location(floor_num=200)
        # 检查99区99栋200层被注册
        result = self.sj.app_get_location(comm_num=99, build_num=99, floor_num=200)
        self.assertTrue(result.get('is_comm_reg') and result.get('is_build_reg') and result.get('is_floor_reg'))
        # 返回且不保存
        self.sj.driver.find_element_by_id('com.fhsj.jbqbl.launcher:id/location_back_btn').click()
        self.sj.driver.find_element_by_name('不保存').click()


if __name__ == "__main__":
    # unittest.main(verbosity=2)
    run_suite(Location)
