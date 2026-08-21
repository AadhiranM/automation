# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from utilities.readproperties import Readconfig
#
# @pytest.fixture(scope="session")  #session  #function
# def driver():
#     # Setup Chrome browser once per test session
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#     driver.get(Readconfig.getapplicationURL())
#     yield driver
#     driver.quit()
#
#
#

import pytest
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utilities.readproperties import Readconfig


@pytest.fixture(scope="session")
def driver(request):

    browser = request.config.getoption("--browser")

    if browser == "chrome":

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            )
        )

    elif browser == "firefox":

        driver = webdriver.Firefox(
            service=FirefoxService(
                GeckoDriverManager().install()
            )
        )

    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(
            f"Unsupported browser: {browser}"
        )

    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get(Readconfig.getapplicationURL())

    yield driver

    driver.quit()


def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )