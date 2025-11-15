import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.manufacturer.mf_login_page import Loginpage  # Import your page object class
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig

class Test_001_login:
    baseURL = Readconfig.getapplicationURL()
    username = Readconfig.getUsername()
    password = Readconfig.getUserpassword()
    logger = LogGen.loggen()


    # baseURL = "https://opensource-demo.orangehrmlive.com/"
    # username = "Admin"
    # password = "admin123"


    @pytest.fixture(scope="class")
    def setPath(self, request):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.baseURL)
        driver.maximize_window()
        request.cls.driver = driver  # Attach driver to the test class
        yield
        driver.quit()

    @pytest.mark.usefixtures("setPath")  # Ensure the fixture is used
    def test_homepageTitle(self):

        self.driver.implicitly_wait(10)
        self.logger.info("**************** test_login *************")
        self.logger.info("**************** verifying Homepage  *************")
        act_title = self.driver.title
        if act_title == "OrangeHRM":
            assert True
            self.logger.info("**************** Homepage title is passed  *************")
        else:
            self.driver.save_screenshot(".\\screenshots\\" + "test_homepageTitle.png")
            assert False
            self.logger.error("**************** Homepage title is failed*************")


    @pytest.mark.usefixtures("setPath")
    def test_login(self):
        self.lp = Loginpage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        # Wait for the dashboard to load
        WebDriverWait(self.driver, 10).until(EC.title_contains("OrangeHRM"))
        act_title = self.driver.title
        if act_title == "OrangeHRM":
            assert True
        else:
            self.driver.save_screenshot(".\\screenshots\\" + "test_login.png")
            assert False

        # Logout after successful login
        self.lp.clickLogout()
