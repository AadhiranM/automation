import pytest
import time
from selenium.webdriver.common.by import By

from PAGES.common.AccessCodePage import AccessCodePage
from PAGES.QR_Management.login_page import Loginpage
from PAGES.User_Management.Roles_and_Permission.create import Roles_and_permission_create
from PAGES.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from PAGES.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Roles_and_permission_create")

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_UM_Roles_and_permission_create(BaseTest):

    logger = LogGen.loggen()

    def test_Roles_and_permission_create(self, driver, data):

        Role_name = data["Role_name"]
        User_type = data["User_type"]
        select_status = data["select_status"]

        self.logger.info(
            f"===== Roles_and_permission_create ====="
        )
        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()

            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # ---------------------------
        # NAVIGATION
        # ---------------------------
        UM_roles_and_per = Roles_and_permission_create(driver)
        UM_roles_and_per.Click_Dashboard()
        UM_roles_and_per.Click_User_management()
        UM_roles_and_per.Click_roles_and_permission()
        UM_roles_and_per.Click_create()
        UM_roles_and_per.Enter_role_name(Role_name)
        UM_roles_and_per.select_user_type(User_type)
        UM_roles_and_per.select_status(select_status)
        UM_roles_and_per.select_check_all_btn()
        UM_roles_and_per.Click_submit_btn()

        try:
            WebDriverWait(driver,10).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "Role created successfully"
                )
            )
            self.logger.info(
                f"Role created successfully | "
            )

        except:
            take_screenshot(
                driver,
                test_name="UM_Role_create_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )
            self.logger.error(
                f"Role creation failed | "
            )
            assert False






