from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        return self.find_element(locator).text

    def is_element_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def wait_for_url(self, expected_url):
        self.wait.until(EC.url_to_be(expected_url))

    def get_current_url(self):
        return self.driver.current_url
