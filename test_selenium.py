"""
@Time    : 2026/1/4 10:18
@Author  : yan.wang
"""
# 导入Selenium的webdriver模块
import time

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class TestCookieLogin:
    def setup_class(self):
        chrome_options = Options()
        # 基础配置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--start-maximized')  # 最大化窗口
        chrome_options.add_argument('--disable-infobars')  # 禁用信息栏
        
        # 性能优化参数 - 加速启动
        chrome_options.add_argument('--disable-background-networking')  # 禁用后台网络
        chrome_options.add_argument('--disable-background-timer-throttling')  # 禁用后台定时器节流
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')  # 禁用被遮挡窗口的后台处理
        chrome_options.add_argument('--disable-breakpad')  # 禁用崩溃报告
        chrome_options.add_argument('--disable-client-side-phishing-detection')  # 禁用客户端钓鱼检测
        chrome_options.add_argument('--disable-component-update')  # 禁用组件更新
        chrome_options.add_argument('--disable-default-apps')  # 禁用默认应用
        chrome_options.add_argument('--disable-hang-monitor')  # 禁用挂起监控
        chrome_options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止
        chrome_options.add_argument('--disable-prompt-on-repost')  # 禁用重新提交提示
        chrome_options.add_argument('--disable-sync')  # 禁用同步
        chrome_options.add_argument('--disable-translate')  # 禁用翻译
        chrome_options.add_argument('--metrics-recording-only')  # 仅记录指标
        chrome_options.add_argument('--no-first-run')  # 跳过首次运行设置
        chrome_options.add_argument('--safebrowsing-disable-auto-update')  # 禁用安全浏览自动更新
        chrome_options.add_argument('--enable-automation')  # 启用自动化
        chrome_options.add_argument('--password-store=basic')  # 使用基础密码存储
        chrome_options.add_argument('--use-mock-keychain')  # macOS上使用模拟钥匙串

        # 设置性能偏好
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.media_stream": 2,
            # "profile.managed_default_content_settings.images": 2,  # 可选：禁用图片加载以加速（注释掉，避免影响页面显示）
        })
        
        # 设置页面加载策略为 eager（不等待所有资源加载完成，加速页面加载）
        # 在 Selenium 4 中，通过设置 page_load_strategy 属性
        chrome_options.page_load_strategy = 'eager'

        # 使用Service指定驱动路径
        service = Service(r'/Users/yanwang/Documents/03dev/tools/chromedriver')

        # 创建驱动实例
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 设置页面加载超时
        self.driver.set_page_load_timeout(30)  # 设置页面加载超时为30秒


    def test_get_cookies(self):
        # 1. 访问企业微信主页/登录页面
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        # 2. 等待20s，人工扫码操作
        time.sleep(20)
        # 3. 等成功登陆之后，再去获取cookie信息
        cookie = self.driver.get_cookies()
        # 4. 将cookie存入一个可持久存储的地方，文件
        # 打开文件的时候添加写入权限
        with open("datas/cookie.yaml", "w") as f:
            # 第一个参数是要写入的数据
            yaml.safe_dump(cookie, f)

    def test_add_cookie(self):
        # 1. 访问企业微信主页面
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        # 2. 定义cookie，cookie信息从已经写入的cookie文件中获取
        cookie = yaml.safe_load(open("datas/cookie.yaml"))
        # 3. 植入cookie
        for c in cookie:
            self.driver.add_cookie(c)
        time.sleep(10)
        # 4.再次访问企业微信页面，发现无需扫码自动登录，而且可以多次使用
        self.driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")

