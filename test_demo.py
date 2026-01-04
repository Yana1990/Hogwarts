"""
@Time    : 2026/1/4 12:06
@Author  : yan.wang
"""
# test_wework_contact.py
import time

import yaml
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestWeworkContact:

    def setup_class(self):
        self.fake = Faker("zh_CN")
        # service = Service(executable_path="./chrome_driver/chromedriver")
        # self.driver = webdriver.Chrome(service=service)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#index")
        time.sleep(1)
        # 从文件中获取 cookie 信息登陆
        with open("datas/cookie.yaml", "r", encoding="utf-8") as f:
            cookies = yaml.safe_load(f)
        print(f"读取出来的cookie:{cookies}")
        for cookie in cookies:
            try:
                # 添加 cookie
                self.driver.add_cookie(cookie)
            except Exception as e:
                print(e)
        time.sleep(3)
        self.driver.refresh()

    def teardown_class(self):
        self.driver.quit()

    def test_ceshiren(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#contact")
