
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
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Login successful (first iteration)")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        UM_create = user_create(driver)
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
            UM_create.select_Role(select_Role)

        if select_status:
            UM_create.Choose_select_status(select_status)

        if Mobile_number:
            UM_create.Enter_Mobile_number(Mobile_number)

        if password:
            UM_create.Enter_password(password)

        UM_create.Click_submit_btn()

        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "User created successfully"
                )
            )
            self.logger.info("User created successfully")

        except:
            take_screenshot(
                driver,
                test_name="UM_user_create_fail",
                folder_name="Screenshots\\User_Management\\Users"
            )
            self.logger.error(
                f"User creation failed | Took screenshot "
            )
            assert False






