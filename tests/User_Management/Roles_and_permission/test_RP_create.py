# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.User_Management.Roles_and_Permission.create import Roles_and_permission_create
# from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
# from utilities.customlogger import LogGen
# from utilities.readproperties import Readconfig
# from utilities.read_excel import get_test_data
# from pages.common.base_page import BaseTest
# from utilities.screenshot_util import take_screenshot
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
# # ---------------------------
# # LOAD EXCEL DATA
# # ---------------------------
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "Roles_and_permission_create")
#
# @pytest.mark.order(1)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_RP_create(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_Roles_and_permission_create(self, driver, data):
#
#         Role_name = data["Role_name"]
#         User_type = data["User_type"]
#         select_status = data["select_status"]
#
#         self.logger.info(
#             f"===== Roles_and_permission_create ====="
#         )
#         # ---------------------------
#         # LOGIN (ONLY ONCE)
#         # ---------------------------
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#
#             self.logger.info("Login successful (first iteration)")
#         else:
#             self.logger.info("Skipping login — already logged in")
#
#         # ---------------------------
#         # NAVIGATION
#         # ---------------------------
#         UM_roles_and_per = Roles_and_permission_create(driver)
#         UM_roles_and_per.Click_Dashboard()
#         UM_roles_and_per.Click_User_management()
#         UM_roles_and_per.Click_roles_and_permission()
#         UM_roles_and_per.Click_create()
#         UM_roles_and_per.Enter_role_name(Role_name)
#         UM_roles_and_per.select_user_type(User_type)
#         time.sleep(1)
#         UM_roles_and_per.select_status(select_status)
#         UM_roles_and_per.select_check_all_btn()
#         UM_roles_and_per.Click_submit_btn()
#
#
#         try:
#             toast_text = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             print("Toast:", toast_text)
#
#         # VALIDATION
#         if toast_text and "Role created successfully" in toast_text:
#             self.logger.info(f"Role created successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_create_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission"
#             )
#             self.logger.error(f"Role creation failed | Toast: {toast_text}")
#             assert False, f"Role creation failed | Toast: {toast_text}"
#
#
#
#

import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.User_Management.Roles_and_Permission.create import Roles_and_permission_create
from utilities.customlogger import LogGen
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
test_data = get_test_data(excel_path, "Roles_and_permission_create")

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_UM_RP_create(BaseTest):

    logger = LogGen.loggen()

    def test_Roles_and_permission_create(self, driver, data):

        Role_name = data["Role_name"]
        User_type = data["User_type"]
        select_status = data["select_status"]

        # ---------------------------
        # START
        # ---------------------------
        self.logger.info(
            f"===== START TEST | Roles_and_permission_create | ROLE={Role_name} ====="
        )

        # ---------------------------
        # LOGIN
        # ---------------------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # ---------------------------
        # ACTION FLOW
        # ---------------------------
        UM_roles_and_per = Roles_and_permission_create(driver)

        self.logger.info("Navigating to Roles & Permission module")
        UM_roles_and_per.Click_Dashboard()
        UM_roles_and_per.Click_User_management()
        UM_roles_and_per.Click_roles_and_permission()

        self.logger.info("Opening create role form")
        UM_roles_and_per.Click_create()

        self.logger.info("Filling role details")
        UM_roles_and_per.Enter_role_name(Role_name)
        UM_roles_and_per.select_user_type(User_type)

        time.sleep(1)

        UM_roles_and_per.select_status(select_status)
        UM_roles_and_per.select_check_all_btn()

        self.logger.info("Submitting role creation form")
        UM_roles_and_per.Click_submit_btn()

        # ---------------------------
        # TOAST
        # ---------------------------
        try:
            toast_text = WebDriverWait(driver,7).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text
            print("Toast:", toast_text)

        except TimeoutException:
            toast_text = "Toast message not displayed"
            print("Toast:", toast_text)

        # ---------------------------
        # RESULT
        # ---------------------------
        if toast_text and "Role created successfully" in toast_text:
            self.logger.info(f"Role created successfully | {Role_name} | {toast_text}")
        else:
            take_screenshot(
                driver,
                test_name="UM_Role_create_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )
            self.logger.error(f"Role creation failed | Toast: {toast_text}")
            assert False, f"Role creation failed | Toast: {toast_text}"