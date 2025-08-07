import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import shutil
import tempfile
import random
from endpoints.pet_api import PetAPI
from endpoints.user_api import UserAPI
from pages.cart_page import CartPage
from pages.checkout_page_1 import CheckoutPageOne
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from selenium.webdriver.chrome.options import Options
import allure
import os


@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


@pytest.fixture(scope="function")
def driver(config):
    base_url = config['UI_SAUCEDEMO']['BASE_URL']
    temp_profile_dir = tempfile.mkdtemp()
    chrome_options = Options()

    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument(
        "--disable-features=PasswordCheck,AutofillServerCommunication,PasswordManagerOnboarding,"
        "OptimizationGuideModelDownloading,Translate")

    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    })

    try:
        service = ChromeService(ChromeDriverManager().install())
    except Exception as e:
        pytest.fail(f"Fail is ChromeDriver installation: {e}")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(base_url)

    yield driver

    driver.quit()
    shutil.rmtree(temp_profile_dir, ignore_errors=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Could not take a screenshot due to an error: {e}")


@pytest.fixture(scope="function")
def logged_in_standard_user(driver, config, login_page, products_page):
    login_page.open_url(config['UI_SAUCEDEMO']['BASE_URL'])
    login_page.login(config['UI_SAUCEDEMO']['USERNAME'], config['UI_SAUCEDEMO']['PASSWORD'])
    login_page.wait_for_url("https://www.saucedemo.com/inventory.html")
    return products_page


@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope="function")
def products_page(driver):
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page_1(driver):
    return CheckoutPageOne(driver)


#API
@pytest.fixture(scope="session")
def pet_api_client(config):
    base_url = config['API']['BASE_URL']
    api_key = os.getenv("API_KEY", None)
    return PetAPI(base_url, api_key=api_key)


@pytest.fixture(scope="session")
def user_api_client(config):
    base_url = config['API']['BASE_URL']
    api_key = os.getenv("API_KEY", None)
    return UserAPI(base_url, api_key=api_key)


@pytest.fixture(scope="function")
def created_pet_id(pet_api_client):
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200
    yield pet_id
    pet_api_client.delete_pet(pet_id)


@pytest.fixture(scope="function")
def created_username(user_api_client):
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": user_id,
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    create_user_response = user_api_client.create_user(user_data)
    assert create_user_response.status_code == 200
    yield user_data["username"]
    user_api_client.delete_user(user_data["username"])