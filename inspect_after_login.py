from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import caps, APPIUM_SERVER
import time

options = UiAutomator2Options()
options.platform_name = caps['platformName']
options.automation_name = caps['automationName']
options.device_name = caps['deviceName']
options.app = caps['app']
options.app_package = caps['appPackage']
options.app_activity = caps['appActivity']
options.new_command_timeout = caps.get('newCommandTimeout', 300)

driver = webdriver.Remote(APPIUM_SERVER, options=options)
try:
    time.sleep(2)
    # click standard_user autofill
    try:
        el = driver.find_element('accessibility id', 'test-standard_user')
        el.click()
        print('Clicked standard_user')
    except Exception as e:
        print('Could not click standard_user:', e)
    # fill password
    try:
        pwd = driver.find_element('accessibility id', 'test-Password')
        pwd.clear()
        pwd.send_keys('secret_sauce')
        print('Password filled')
    except Exception as e:
        print('Could not set password:', e)
    # click login
    try:
        btn = driver.find_element('accessibility id', 'test-LOGIN')
        btn.click()
        print('Clicked login')
    except Exception as e:
        print('Could not click login:', e)
    time.sleep(3)
    src = driver.page_source
    with open('page_after_login.xml','w',encoding='utf-8') as f:
        f.write(src)
    print('Saved page_after_login.xml')
finally:
    driver.quit()
    print('Driver quit')
