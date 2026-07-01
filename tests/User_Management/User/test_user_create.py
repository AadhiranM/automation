# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.User_Management.Users.user_create import user_create
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
# test_data = get_test_data(excel_path, "users_create")
#
# @pytest.mark.order(1)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_users_create(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_users_create(self, driver, data):
#
#         user_name = data["user_name"]
#         select_Role = data["select_Role"]
#         Email = data["Email"]
#         select_status = data["select_status"]
#         Mobile_number = data["Mobile_number"]
#         password = data["password"]
#
#         self.logger.info("===== user_management ==== users ==== create =====")
#
#         # ---------------------------
#         # LOGIN (ONLY ONCE)
#         # ---------------------------
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#             self.logger.info("Login successful (first iteration)")
#         else:
#             self.logger.info("Skipping login — already logged in")
#
#         UM_create = user_create(driver)
#         driver.refresh()
#         UM_create.Click_Dashboard()
#         UM_create.Click_User_management()
#         UM_create.Click_users()
#         UM_create.Click_create()
#
#         # ---------------------------
#         # FILL FORM (ONLY IF DATA EXISTS)
#         # ---------------------------
#
#         if user_name:
#             UM_create.Enter_username(user_name)
#         if Email:
#             UM_create.Enter_Email(Email)
#         if select_Role:
#             UM_create.select_Role_drpdown()
#             UM_create.Enter_Role_input(select_Role)
#         if select_status:
#             UM_create.Choose_select_status(select_status)
#         if Mobile_number:
#             UM_create.Enter_Mobile_number(Mobile_number)
#         if password:
#             UM_create.Enter_password(password)
#         UM_create.Click_submit_btn()
#
#         try:
#             toast_text = WebDriverWait(driver,10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             print("Toast:", toast_text)
#
#         # VALIDATION
#         if toast_text and "User created successfully" in toast_text:
#
#             self.logger.info(f"Roles and permission | User created successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_user_create_fail",
#                 folder_name="Screenshots\\User_Management\\Users\\create"
#             )
#             self.logger.error(f"Roles and permission | User creation failed | Toast: {toast_text}")
#             assert False, f"User creation failed | Toast: {toast_text}"
#
#

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


@pytest.mark.order(1)
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

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== User Creation Test Started | User: {user_name} ====="
        )

        self.logger.info(
            f"User Details | Username: {user_name} | Role: {select_Role} | "
            f"Email: {Email} | Status: {select_status}"
        )

        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        # if data == test_data[0]:
        #
        #     self.logger.info("Executing login flow for first iteration")
        #
        #     self.driver = driver
        #     self.login_and_access()
        #
        #     self.logger.info("Login successful (first iteration)")
        #
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # =========================
        # NAVIGATION LOGS
        # =========================
        self.logger.info("Refreshing browser")

        UM_create = user_create(driver)
        driver.refresh()

        self.logger.info("Navigating to Dashboard")
        UM_create.Click_Dashboard()

        self.logger.info("Opening User Management module")
        UM_create.Click_User_management()

        self.logger.info("Opening Users page")
        UM_create.Click_users()

        self.logger.info("Opening Create User form")
        UM_create.Click_create()

        # =========================
        # FORM FILL LOGS
        # =========================
        self.logger.info("Entering user details")

        if user_name:
            self.logger.info(f"Entering Username: {user_name}")
            UM_create.Enter_username(user_name)

        if Email:
            self.logger.info(f"Entering Email: {Email}")
            UM_create.Enter_Email(Email)

        if select_Role:
            self.logger.info(f"Selecting Role: {select_Role}")
            UM_create.select_Role_drpdown()
            UM_create.Enter_Role_input(select_Role)

        if select_status:
            self.logger.info(f"Selecting Status: {select_status}")
            UM_create.Choose_select_status(select_status)

        if Mobile_number:
            self.logger.info(f"Entering Mobile Number: {Mobile_number}")
            UM_create.Enter_Mobile_number(Mobile_number)

        if password:
            self.logger.info("Entering Password")
            UM_create.Enter_password(password)

        # =========================
        # SUBMIT ACTION
        # =========================
        self.logger.info("Submitting user creation form")

        UM_create.Click_submit_btn()

        # =========================
        # TOAST HANDLING
        # =========================
        self.logger.info("Waiting for toast response")

        try:
            toast_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text.strip()
            toast_text = toast_text.encode("ascii", errors="ignore").decode()
            print("Toast:", toast_text)

            self.logger.info(f"Toast received | {toast_text}")

        except TimeoutException:

            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error(
                "Toast message not displayed within timeout"
            )

        # =========================
        # FINAL VALIDATION
        # =========================
        if toast_text and "User created successfully" in toast_text:

            self.logger.info(
                f"User created successfully | Username: {user_name} | {toast_text}"
            )

        else:

            self.logger.error(
                f"User creation failed | Username: {user_name} | Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="UM_user_create_fail",
                folder_name="Screenshots\\User_Management\\Users\\create"
            )

            assert False, (
                f"User creation failed | Toast: {toast_text}"
            )
