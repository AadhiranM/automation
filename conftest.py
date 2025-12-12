import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utilities.readproperties import Readconfig

@pytest.fixture(scope="session")  #session  #function
def driver():
    # Setup Chrome browser once per test session
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(Readconfig.getapplicationURL())
    yield driver
    driver.quit()



