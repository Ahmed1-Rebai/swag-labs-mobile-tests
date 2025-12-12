from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    # Accepted usernames shown on the screen for autofill
    ACCEPTED_STANDARD = (AppiumBy.ACCESSIBILITY_ID, "test-standard_user")
    ERROR_MSG = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'error') or contains(@text, 'Error')]")


    def login(self, username, password):
        by, value = self.USERNAME
        self.send_keys(by, value, username)
        by, value = self.PASSWORD
        self.send_keys(by, value, password)
        self.click(*self.LOGIN_BTN)


    def get_error(self):
        try:
            return self.find(*self.ERROR_MSG).text
        except:
            return "No error message found"
