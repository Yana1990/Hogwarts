"""
@Time    : 2026/1/4 14:41
@Author  : yan.wang
"""
import allure

from base.base_page import BasePage


class AddMemberPage(BasePage):


    @allure.step("输入成员信息，点击保存按钮，跳转通讯录页面")
    def input_member_info(self, mname, mid, phone_num):
        '''
        输入成员信息，点击保存按钮，跳转通讯录页面
        :return:
        '''
