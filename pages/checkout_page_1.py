from selenium.webdriver.common.by import By
from faker import Faker
from pages.base_page import BasePage
from pages.checkout_page_2 import CheckoutPageTwo


class CheckoutPageOne(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE_BUTTON = (By.XPATH, "//h3[@data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def generate_checkout_data(self) -> dict:
        faker = Faker('uk_UA')
        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "postal_code": faker.postcode()
        }
        return test_data

    def generate_checkout_data_with_empty_zip(self) -> dict:
        faker = Faker('uk_UA')
        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "postal_code": ""
        }
        return test_data

    def fill_checkout_form(self, data):
        self.enter_text(self.FIRST_NAME_INPUT, data["first_name"])
        self.enter_text(self.LAST_NAME_INPUT, data["last_name"])
        self.enter_text(self.POSTAL_CODE_INPUT, data["postal_code"])

    def click_continue_button(self):
        self.click_element(self.CONTINUE_BUTTON)
        if self.is_error_message_displayed():
            return self
        else:
            return CheckoutPageTwo(self.driver)

    def is_error_message_displayed(self):
        return self.is_element_displayed(self.ERROR_MESSAGE_BUTTON)

    def get_error_message_text(self):
        return self.get_element_text(self.ERROR_MESSAGE_BUTTON)