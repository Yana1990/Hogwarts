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

    def test_add_member(self):
        '''
        添加成员
        :return:
        '''
        # 数据准备
        # 姓名
        mname = self.fake.name()
        # 账号
        mid = self.fake.uuid4()
        # 手机号
        phone_num = self.fake.phone_number()
        # 点击通讯录按钮
        self.driver.find_element(
            By.XPATH,
            "//*[@id='nav']//*[text()='通讯录']"
        ).click()
        # 等待组织架构按钮可被点击
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//*[@id='nav']//*[text()='组织架构']")
            )
        )
        # 点击展开的二级菜单中的组织架构按钮
        self.driver.find_element(
            By.XPATH,
            "//*[@id='nav']//*[text()='组织架构']"
        ).click()
        # 进入通讯录页面
        # 显式等待成员列表加载完毕
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.ID, "member_list")
            )
        )
        # 点击添加成员按钮
        self.driver.find_element(
            By.CSS_SELECTOR,
            ".member_operationBar .js_add_member"
        ).click()
        # 显式等待输入姓名出现
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.ID, "username")
            )
        )
        # 输入姓名
        self.driver.find_element(
            By.ID, "username"
        ).send_keys(mname)
        # 输入账号
        self.driver.find_element(
            By.ID, "memberAdd_acctid"
        ).send_keys(mid)
        # 输入手机号
        self.driver.find_element(
            By.ID, "memberAdd_phone"
        ).send_keys(phone_num)
        # 点击保存按钮
        save_btn = self.driver.find_element(By.CSS_SELECTOR, ".qui_btn.ww_btn.js_btn_save")
        self.driver.execute_script("arguments[0].click();", save_btn)
        # 获取保存结果提示信息
        tips = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "js_tips")
            )
        )
        # 根据提示信息断言
        assert tips.text == "保存成功"
        # 等待成员列表加载完毕
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "member_list")
            )
        )
        # 获取成员列表信息
        # 定位 .member_colRight_memberTable_td 同一级兄弟元素中的第二个
        names = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".member_colRight_memberTable_td:nth-child(2)"
        )
        # 使用列表推导式获取成员姓名，放入列表
        name_list = [n.text for n in names]
        # 断言新添加成员姓名在列表中
        assert mname in name_list
