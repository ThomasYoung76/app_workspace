"""
    Function: 
"""
import sys
sys.path.append('.')
from libs.func import *
from scripts.test_board import Board
from scripts.test_device_manage import DeviceManage
from scripts.test_linkage import TestLinkage
from scripts.test_login import Login
from scripts.test_location import Location
from scripts.test_query import QueryRecord
from scripts.test_terminal import Terminal
from scripts.test_user_manage import UserManage

if __name__ == "__main__":
    suite_class = ['Board', 'Device', 'TestLinkage', 'Login', 'Location', 'QueryRecord', 'UserManage']
    run_suite(suite_class)