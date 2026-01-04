"""
@Time    : 2026/1/4 14:41
@Author  : yan.wang
"""
import allure

from base.base_page import BasePage


class MainPage(BasePage):

    @allure.step("登录企业微信 web 端，进入首页")
    def login(self):
        """
        登录，进入首页
        :return:
        """
