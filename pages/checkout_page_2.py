from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutComplete


class CheckoutPageTwo(BasePage):
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        super().__init__(driver)

    def get_item_total(self):
        return self.get_element_text(self.ITEM_TOTAL)

    def get_tax(self):
        return self.get_element_text(self.TAX)

    def get_total(self):
        return self.get_element_text(self.TOTAL)

    def click_finish_button(self):
        self.click_element(self.FINISH_BUTTON)
        assert self.get_current_url() == "https://www.saucedemo.com/checkout-complete.html"
        return CheckoutComplete(self.driver)


