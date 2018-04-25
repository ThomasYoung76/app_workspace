# coding: utf-8
"""
    测试数据
"""
import os

APP_HOME = os.path.dirname(os.getcwd())
APP_RESULT = os.path.join(APP_HOME, 'result')
LOG_PATH = APP_HOME + os.sep + 'log'
# 登录用户
sys_user_name = '系统管理员'
sys_user_num = 1
adj_user_num = 2
raw_password = '88888888'
err_password1 = '12345678'
err_password2 = '62633134'
err_password3 = '11111111'
err_password4 = '11111111'
err_password5 = '11111111'

sys_admin = '系统管理员'
adjustor = '调试员'
supKeeper = '值班管理员'
keeper = '值班员'

# 用户均为初始密码
params_sys = [('sysadmin', 1, '88888888')]  # 系统管理员初始密码
params_adj = [('adjustor', 2, '88888888')]  # 调试员初始密码
params_sup = [('supKeeper', 3, '888888')]   # 值班管理员密码
params_keeper = [('keeper', 4, '8888')]     # 值班员密码
params_sys_err = [('sysadmin', 1, '12345678')]  # 系统管理员错误的密码
# 系统管理员
user_num = 1
user_password = '88888888'

# 衍生用于参数化测试用户的参数
params_all = params_sys + params_adj + params_sup + params_keeper
params_raw = params_sys + params_adj + params_sup

# 是否打印日志
is_print = True

# 联动设置需要的参数
param_linkage_block_index = [(1,), (2,), (3,), (6,)]
param_linkage_layer_index = [(4,), (5,)]
param_linkage_index = param_linkage_layer_index + param_linkage_block_index
