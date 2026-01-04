"""
@Time    : 2026/1/4 14:41
@Author  : yan.wang
"""
import allure

from base.base_page import BasePage


class ContactPage(BasePage):

    @allure.step("点击添加成员按钮，进入添加成员界面")
    def goto_add_member_page(self):
        '''
        点击添加成员按钮，进入添加成员界面
        :return:
        '''

    @allure.step("获取通讯录用户列表")
    def get_contact_member_list(self):
        '''
        获取通讯录用户列表
        :return:
        '''