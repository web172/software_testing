from selenium import webdriver
from selenium.webdriver.chrome.service import Service
def test_login_page():
    driver_path = "/opt/homebrew/bin/chromedriver"
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service) # 或 Firefox()
    driver.get("http://127.0.0.1:5000/login")
    assert "登录" in driver.page_source
    driver.quit()