Test Automation Project
Description
This project is designed for the automated UI testing of the https://www.saucedemo.com/ website using Selenium. Additionally, it includes API testing for the Petstore REST API service. Dependency management is handled through pyproject.toml and the uv package manager.

Features
UI Testing: Utilizes the Selenium library for web browser automation.

API Testing: Uses the httpx library for sending HTTP requests.

Dependency Management: Centralized via the pyproject.toml file and the uv tool.

Testing Framework: Uses pytest.

Reporting: Generates detailed reports using Allure.

Prerequisites
Python: Version 3.12 or higher.

Git: Installed on your system.

Installation and Setup
Clone the repository:

git clone https://github.com/gityaroslav/qa_automation_ui_and_api
cd qa-automation-project

Create a virtual environment and install dependencies:
This project uses uv. The sync command will create a virtual environment and install all packages specified in pyproject.toml, including Selenium.

uv sync

After installation, activate the virtual environment if needed.

Configuration
Environment Variables
Some tests require an API key. You must pass it as an environment variable named API_KEY.

To run in PyCharm:

Go to the Run > Edit Configurations... menu.

Select the desired configuration or create a new one.

In the Environment variables section, add a new variable:

Name: API_KEY

Value: [your_secret_key]

Configuration File
Some API settings (e.g., BASE_URL) are located in the config.ini file. Update it if necessary.

Running Tests
To run all tests in the project, use pytest.

pytest

To run tests and generate an Allure report, use the command:

pytest --alluredir=allure-results

Viewing Allure Reports
After generating the reports, you can view them in your browser by running the command:

allure serve allure-results

Author: Slava

Email: slavk0@ukr.net