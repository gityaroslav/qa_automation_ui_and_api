
class TestLoginPage:

    def test_successful_login_with_standard_user(self, driver, config, login_page, products_page):
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert products_page.get_current_url() == expected_url
        assert products_page.is_products_page_displayed()
        assert products_page.get_products_title_text() == "Products"

    def test_login_with_locked_user(self, driver, config, login_page):
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        login_page.login(config['UI_SAUCEDEMO']['LOCKED_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        expected_url = "https://www.saucedemo.com/"
        assert login_page.get_current_url() == expected_url
        assert login_page.get_error_message().lower() == "epic sadface: sorry, this user has been locked out."

    def test_login_with_problem_user(self, driver, config, login_page, products_page):
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        login_page.login(config['UI_SAUCEDEMO']['PROBLEM_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert products_page.get_current_url() == expected_url
        assert products_page.is_products_page_displayed()
        assert products_page.get_products_title_text() == "Products"

    def test_performance_glitch_user(self, driver, config, login_page, products_page):
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        login_page.login(config['UI_SAUCEDEMO']['PERFORMANCE_GLITCH_USER'], config['UI_SAUCEDEMO']['PASSWORD'])
        login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert products_page.get_current_url() == expected_url
        assert products_page.is_products_page_displayed()
        assert products_page.get_products_title_text() == "Products"

    def test_login_with_invalid_password(self, driver, config, login_page):
        login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
        login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['INVALID_PASSWORD'])
        expected_url = "https://www.saucedemo.com/"
        assert login_page.get_current_url() == expected_url
        expected_error_message = "Epic sadface: Username and password do not match any user in this service"
        actual_error_message = login_page.get_error_message()
        assert actual_error_message.lower() == expected_error_message.lower()

