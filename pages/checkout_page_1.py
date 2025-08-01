from selenium.webdriver.common.by import By
from faker import Faker

from pages.base_page import BasePage
from pages.checkout_page_2 import CheckoutPageTwo


class CheckoutPageOne(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def __init__(self, driver):
        super().__init__(driver)

    def generate_checkout_data(self) -> dict:
        """
        Генерує випадкові дані для форми оформлення замовлення за допомогою Faker.
        Повертає словник з даними.
        """
        faker = Faker('uk_UA')
        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "postal_code": faker.postcode()
        }
        return test_data

    def fill_checkout_form_and_continue(self, data):
        self.enter_text(self.FIRST_NAME_INPUT, data["first_name"])
        self.enter_text(self.LAST_NAME_INPUT, data["last_name"])
        self.enter_text(self.POSTAL_CODE_INPUT, data["postal_code"])
        self.click_element(self.CONTINUE_BUTTON)
        assert self.get_current_url() == "https://www.saucedemo.com/checkout-step-two.html"
        return CheckoutPageTwo(self.driver)
