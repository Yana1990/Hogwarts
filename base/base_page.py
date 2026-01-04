"""
@Time    : 2026/1/4 14:40
@Author  : yan.wang
"""
import os
import time

import allure
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils.log_uitls import logger


class BasePage:

    def __init__(self, driver=None):
        if driver == None:
            # service = Service(executable_path="../../chrome_driver/chromedriver")
            # self.driver = webdriver.Chrome(service=service)
            self.driver = webdriver.Chrome()
        else:
            self.driver = driver
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def close_browser(self):
        '''
        关闭浏览器
        :return:
        '''
        self.driver.quit()

    def open_url(self, url):
        '''
        打开网页
        :param url: 要打开页面的 url
        :return:
        '''
        self.driver.get(url)

    def find_ele(self, by, value):
        '''
        查找单个元素
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :return: 找到的元素对象
        '''
        logger.info(f"定位单个元素，定位方式为 {by}, 定位表达式为 {value}")
        try:
            ele = self.driver.find_element(by, value)
        except Exception as e:
            ele = None
            logger.info(f"单个元素没有找到{ele}")
            # 截图
            self.screen_image()
            self.save_page_source()
        return ele

    def find_eles(self, by, value):
        '''
        查找多个元素
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :return: 元素列表
        '''
        logger.info(f"定位一组元素，定位方式为 {by}, 定位表达式为 {value}")
        try:
            eles = self.driver.find_elements(by, value)
        except Exception as e:
            eles = None
            logger.info(f"该组元素没有找到{eles}）")
            # 截图
            self.screen_image()
            self.save_page_source()
        return eles

    def find_and_get_text(self, by, value):
        '''
        获取单个元素的文本属性
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :return: 文本内容
        '''
        text_value = self.find_ele(by, value).text
        return text_value

    def click_ele(self, by, value):
        '''
        查找单个元素并点击
        :param by: 元素定位方式
        :param value: 元素定位表达式
        '''
        self.find_ele(by, value).click()

    def ele_sendkeys(self, by, value, text):
        '''
        单个元素输入内容
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :param text: 要输入的内容字符串
        '''
        # 清除内容
        self.find_ele(by, value).clear()
        # 输入内容
        self.find_ele(by, value).send_keys(text)

    def wait_ele_located(self, by, value, timetout=10):
        '''
        显式等待元素可以被定位
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :param timetout: 等待时间
        :return: 定位到的元素对象
        '''
        ele = WebDriverWait(self.driver, timetout).until(
            expected_conditions.visibility_of_element_located((by, value))
        )
        return ele

    def wait_ele_click(self, by, value, timeout=10):
        '''
        显式等待元素可以被点击
        :param by: 元素定位方式
        :param value: 元素定位表达式
        :param timeout: 等待时间
        '''
        ele = WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable((by, value))
        )
        return ele

    def login_by_cookie(self):
        '''
        通过 cookie 登录
        :return:
        '''
        # 从文件中获取 cookie 信息登陆
        with open("../datas/cookie.yaml", "r", encoding="utf-8") as f:
            cookies = yaml.safe_load(f)
        print(f"读取出来的cookie:{cookies}")
        for cookie in cookies:
            # 添加 cookie
            self.driver.add_cookie(cookie)
        # 刷新页面
        self.driver.refresh()

    def click_ele_by_js(self, ele):
        '''
        使用 js 的方式点击元素
        :param ele: 元素对象
        :return:
        '''
        self.driver.execute_script("arguments[0].click();", ele)

    def get_path(self, path_name):
        '''
        获取绝对路径
        :param path_name: 目录名称
        :return: 目录绝对路径
        '''
        # 获取当前工具文件所在的路径
        root_path = os.path.dirname(os.path.abspath(__file__))
        # 拼接当前要输出日志的路径
        dir_path = os.sep.join([root_path, '..', f'/{path_name}'])
        return dir_path

    def screen_image(self):
        '''
        截图
        :return: 图片保存路径
        '''
        # 截图命名
        now_time = time.strftime('%Y_%m_%d_%H_%M_%S')
        image_name = f"{now_time}.png"
        # 拼接截图保存路径
        # windows f"{self.get_path('image')}\\{image_name}"
        image_path = f"{self.get_path('image')}/{image_name}"
        logger.info(f"截图保存路径为 {image_path}")
        # 截图
        self.driver.save_screenshot(image_path)
        # 添加截图到 allure
        allure.attach.file(image_path, name="查找元素异常截图",
                           attachment_type=allure.attachment_type.PNG)
        return image_path

    def save_page_source(self):
        '''
        保存页面源码
        :return: 页面源码保存路径
        '''
        # 文件命名
        now_time = time.strftime('%Y_%m_%d_%H_%M_%S')
        pagesource_name = f"{now_time}_pagesource.html"
        # 拼接文件保存路径
        # windows f"{self.get_path('pagesource')}\\{pagesource_name}"
        pagesource_path = f"{self.get_path('pagesource')}/{pagesource_name}"
        logger.info(f"页面源码文件保存路径为 {pagesource_path}")
        # 保存 page source
        with open(pagesource_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        # pagesource 添加到 allure 报告
        allure.attach.file(pagesource_path,name="查找元素异常的页面源码",
                           attachment_type=allure.attachment_type.TEXT)
        return pagesource_path
