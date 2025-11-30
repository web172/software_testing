import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# 全局配置
BASE_URL = "http://fecyo.fecshop.com/cn/"
TEST_PHONE = "13812348886"  # 未注册测试手机号（可替换）
REGISTERED_PHONE = "13812348887"  # 已注册手机号（需提前注册）
TEST_PASSWORD = "Abc123456"
WRONG_PASSWORD = "123456"
UNREGISTERED_PHONE = "13912349999"


class TestFecyoShop:
    # 初始化浏览器
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    # 清理环境
    def teardown_method(self):
        self.driver.quit()

    # 辅助方法：获取元素
    def get_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    # ------------------------------ 注册模块测试（适配页面源码） ------------------------------
    def test_register_normal(self):
        """REG-001：手机号正常注册"""
        self.driver.get(f"{BASE_URL}customer/account/register")

        # 输入手机号（适配id="phone"、name="editForm[phone]"）
        mobile_input = self.get_element(By.ID, "phone")
        mobile_input.clear()
        mobile_input.send_keys(TEST_PHONE)

        # 输入密码（适配id="password"、name="editForm[password]"）
        pwd_input = self.get_element(By.ID, "password")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 输入确认密码（适配id="confirmation"、name="editForm[confirmation]"）
        confirm_pwd_input = self.get_element(By.ID, "confirmation")
        confirm_pwd_input.clear()
        confirm_pwd_input.send_keys(TEST_PASSWORD)

        # 点击注册按钮（适配id="register-btn"，span标签）
        register_btn = self.get_element(By.ID, "register-btn")
        register_btn.click()
        time.sleep(3)  # 等待页面响应

        # 断言结果（注册成功跳转登录页，提示信息）
        # 验证跳转URL
        #http://fecyo.fecshop.com/cn/customer/account
        assert self.driver.current_url.endswith("customer/account")
        # 验证成功提示（若页面有提示，可补充断言）

    def test_register_invalid_phone_format(self):
        """REG-002：手机号格式错误注册"""
        self.driver.get(f"{BASE_URL}customer/account/register")

        # 输入5位错误手机号
        mobile_input = self.get_element(By.ID, "phone")
        mobile_input.clear()
        mobile_input.send_keys("12345")

        # 输入密码和确认密码（满足表单提交基础条件）
        pwd_input = self.get_element(By.ID, "password")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        confirm_pwd_input = self.get_element(By.ID, "confirmation")
        confirm_pwd_input.clear()
        confirm_pwd_input.send_keys(TEST_PASSWORD)

        # 点击注册按钮
        register_btn = self.get_element(By.ID, "register-btn")
        register_btn.click()
        time.sleep(2)

        # 断言错误提示（适配class="err-tip phone"，验证文本和显示状态）
        phone_err_tip = self.get_element(By.CLASS_NAME, "err-tip.phone")
        # 验证错误提示已显示（移除hide类）
        assert "hide" not in phone_err_tip.get_attribute("class")
        # 验证错误提示文本（页面JS定义的提示）
        err_text = phone_err_tip.find_element(By.TAG_NAME, "em").text
        assert "Please input the phone" in err_text

    def test_register_already_exist(self):
        """REG-003：已注册账号注册"""
        self.driver.get(f"{BASE_URL}customer/account/register")

        # 输入已注册手机号
        mobile_input = self.get_element(By.ID, "phone")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        # 输入密码和确认密码
        pwd_input = self.get_element(By.ID, "password")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        confirm_pwd_input = self.get_element(By.ID, "confirmation")
        confirm_pwd_input.clear()
        confirm_pwd_input.send_keys(TEST_PASSWORD)

        # 点击注册按钮
        register_btn = self.get_element(By.ID, "register-btn")
        register_btn.click()
        time.sleep(3)

        # 断言结果（已注册手机号的错误提示）
        error_msg = self.get_element(By.CLASS_NAME, "error-msg")
        assert "this phone is exist!" in error_msg.text

    # ------------------------------ 登录模块测试（保持不变，如需适配可补充页面源码） ------------------------------
    def test_login_normal(self):
        """LOG-001：账号密码正常登录"""
        self.driver.get(f"{BASE_URL}customer/account/login/")

        # 输入账号密码（假设登录页用户名输入框name为login[username]，可根据登录页源码调整）
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 点击登录（适配登录页按钮，若有id可替换）
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)

        # 断言结果（验证跳转首页和用户名显示）
        assert self.driver.current_url.endswith("customer/account")


    def test_login_wrong_password(self):
        """LOG-002：密码错误登录"""
        self.driver.get(f"{BASE_URL}customer/account/login/")

        # 输入正确账号和错误密码
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(WRONG_PASSWORD)

        # 点击登录
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)

        # 断言错误提示
        error_msg = self.get_element(By.CLASS_NAME, "error-msg")
        assert "用户的账号密码不正确" in error_msg.text

    def test_login_unregistered(self):
        """LOG-003：未注册账号登录"""
        self.driver.get(f"{BASE_URL}customer/account/login/")

        # 输入未注册账号和任意密码
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(UNREGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 点击登录
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)

        # 断言错误提示
        error_msg = self.get_element(By.CLASS_NAME, "error-msg")
        assert "phone is not exist" in error_msg.text

    #------------------------------ 购物车模块测试（保持不变，如需适配可补充页面源码） ------------------------------
    def test_add_to_cart(self):
        """CAR-001：商品添加至购物车"""
        # 先登录
        self.driver.get(f"{BASE_URL}customer/account/login/")

         # 输入账号密码（假设登录页用户名输入框name为login[username]，可根据登录页源码调整）
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 点击登录（适配登录页按钮，若有id可替换）
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)

        # 进入商品详情页（替换为网站实际商品页，示例用第一个商品）
        self.driver.get(f"{BASE_URL}stylish-striped-criss-cross-womens-dress")


        # 点击加入购物车（适配默认按钮文本）
        add_cart_btn = self.get_element(By.ID, "add-to-cart")
        add_cart_btn.click()
        time.sleep(2)

        # 断言添加成功提示
        success_msg = self.get_element(By.CLASS_NAME, "success-tip")
        assert "该商品已成功添加到购物车" in success_msg.text


    def test_update_cart_quantity(self):
        """CAR-002：修改商品数量（+按钮）"""
        # 先添加商品到购物车
        self.driver.get(f"{BASE_URL}customer/account/login/")

        # 输入账号密码（假设登录页用户名输入框name为login[username]，可根据登录页源码调整）
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 点击登录（适配登录页按钮，若有id可替换）
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)

        # 进入购物车页面
        self.driver.get(f"{BASE_URL}checkout/cart/")

        # 点击数量+按钮（适配购物车数量控件）
        plus_btn = self.get_element(By.CSS_SELECTOR, "span.plus.cart-num-btn")
        plus_btn.click()
        time.sleep(2)

        # 验证数量更新为2
        qty_input = self.get_element(By.CLASS_NAME, "car_ipt")
        assert qty_input.get_attribute("value") == "2"


    def test_delete_cart_item(self):
        """CAR-003：单个商品删除"""
        # 先添加商品到购物车
        self.driver.get(f"{BASE_URL}customer/account/login/")

        # 输入账号密码（假设登录页用户名输入框name为login[username]，可根据登录页源码调整）
        mobile_input = self.get_element(By.NAME, "editForm[phone]")
        mobile_input.clear()
        mobile_input.send_keys(REGISTERED_PHONE)

        pwd_input = self.get_element(By.NAME, "editForm[password]")
        pwd_input.clear()
        pwd_input.send_keys(TEST_PASSWORD)

        # 点击登录（适配登录页按钮，若有id可替换）
        login_btn = self.get_element(By.ID, "login-btn")
        login_btn.click()
        time.sleep(2)


        # 进入购物车页面
        self.driver.get(f"{BASE_URL}checkout/cart/")

        # 点击删除按钮
        delete_btn = self.get_element(By.CSS_SELECTOR, "span[data-role='cart-del-btn']")
        delete_btn.click()
        time.sleep(2)

        # 验证购物车为空
        cart_empty = self.get_element(By.CLASS_NAME, "shop-cart-empty")
        assert "购物车空空的哦，去看看心仪的商品吧~" in cart_empty.text


