import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 全局配置
BASE_URL = "http://fecyo.fecshop.com/cn/"
TEST_PHONE = "138" + str(int(time.time()))[-8:]  # 动态生成11位测试手机号
TEST_PASSWORD = "Test123456"
TEST_PASSWORD_WRONG_CONFIRM = "Test12345"  # 不一致的确认密码

driver = webdriver.Chrome()  # 需提前配置ChromeDriver
driver.implicitly_wait(10)
driver.maximize_window()
driver.get(BASE_URL)
time.sleep(10)
