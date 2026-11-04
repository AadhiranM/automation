
import pytest
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options
from utilities.readproperties import Readconfig

@pytest.fixture(scope="session")
def driver(request):

    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":

        options = ChromeOptions()

        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-extensions")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=options
        )

        for handle in driver.window_handles:
            driver.switch_to.window(handle)

            if "triggeredResetProfileSettings" in driver.current_url:
                driver.close()

        driver.switch_to.window(driver.window_handles[0])
    elif browser == "firefox":

        options = FirefoxOptions()

        if headless:
            options.add_argument("-headless")

        driver = webdriver.Firefox(
            service=FirefoxService(
                GeckoDriverManager().install()
            ),
            options=options
        )

    elif browser == "edge":

        options = EdgeOptions()

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=options
        )

    else:
        raise ValueError(
            f"Unsupported browser: {browser}"
        )

    if not headless:
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

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


###normal browser
#pytest -v -s --browser=chrome

### headless browser mode
#pytest -v -s --browser=chrome --headless


## pytest -v -s --log-cli-level=INFO --browser=chrome --headless -k "Test_login or Test_category" --html=Reports/report.html --self-contained-html

