from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutComplete(BasePage):

    THANK_YOU_TEXT = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        super().__init__(driver)

    def is_thank_you_displayed(self):
        return self.is_element_displayed(self.THANK_YOU_TEXT)