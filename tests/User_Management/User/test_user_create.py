import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.User_Management.Users.user_create import user_create
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "users_create")

@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
class Test_UM_users_create(BaseTest):

    logger = LogGen.loggen()

    def test_users_create(self, driver, data):

        user_name = data["user_name"]
        select_Role = data["select_Role"]
        Email = data["Email"]
        select_status = data["select_status"]
        Mobile_number = data["Mobile_number"]
        password = data["password"]

        self.logger.info("===== user_management ==== users ==== create =====")

        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        UM_create = user_create(driver)
        driver.refresh()
        UM_create.Click_Dashboard()
        UM_create.Click_User_management()
        UM_create.Click_users()
        UM_create.Click_create()

        # ---------------------------
        # FILL FORM (ONLY IF DATA EXISTS)
        # ---------------------------

        if user_name:
            UM_create.Enter_username(user_name)
        if Email:
            UM_create.Enter_Email(Email)
        if select_Role:
            UM_create.select_Role_drpdown()
            UM_create.Enter_Role_input(select_Role)
        if select_status:
            UM_create.Choose_select_status(select_status)
        if Mobile_number:
            UM_create.Enter_Mobile_number(Mobile_number)
        if password:
            UM_create.Enter_password(password)
        UM_create.Click_submit_btn()

        try:
            toast_text= WebDriverWait(driver,7).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text
            if toast_text:
                print("Toast:", toast_text)

        # validation
            if toast_text and "User created successfully" in toast_text:
                self.logger.info("Roles and permission , User created successfully")

        except TimeoutException:
            take_screenshot(
                driver,
                test_name="UM_user_create_fail",
                folder_name="Screenshots\\User_Management\\Users\\create"
            )
            self.logger.error(f"Roles and permission , User creation failed | Took screenshot")
            assert False, "please enter correct details"






