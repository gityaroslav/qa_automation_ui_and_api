from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")
    LOGIN_BOX = (By.CLASS_NAME, "login-box")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)

    def id_login_box_visible(self):
        return self.is_element_displayed(self.LOGIN_BOX)