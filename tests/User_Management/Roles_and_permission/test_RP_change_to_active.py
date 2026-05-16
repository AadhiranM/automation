# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.User_Management.Roles_and_Permission.filters import Roles_and_permission_filters
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
# test_data = get_test_data(excel_path, "Roles_and_permission_filters")
#
# @pytest.mark.order(3)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_RP_change_to_active(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_Roles_and_permission_filters(self, driver, data):
#
#         search_name = data["search_name"]
#         select_status = data["select_status"]
#         start_date = data["start_date"]
#         end_date = data["end_date"]
#
#         self.logger.info(
#             f"===== Roles_and_permission_filters ====="
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
#         UM_roles_and_per_filters = Roles_and_permission_filters(driver)
#         UM_roles_and_per_filters.Click_Dashboard()
#         UM_roles_and_per_filters.Click_User_management()
#         UM_roles_and_per_filters.Click_roles_and_permission()
#         UM_roles_and_per_filters.Enter_search_name_field(search_name)
#         UM_roles_and_per_filters.Choose_select_status(select_status)
#         UM_roles_and_per_filters.Click_filter_calender()
#         UM_roles_and_per_filters.select_date_range(start_date,end_date)
#         status =UM_roles_and_per_filters.search_product(search_name,"Inactive")  # True if rows exist
#
#         if not status:
#             take_screenshot(
#                 driver,
#                 test_name="Roles_and_permission_filter_failed",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission"
#             )
#             self.logger.error("Filter applied but no data found in table")
#             assert status, "No data found after applying filters!"
#         self.logger.info("Filter applied successfully, table has records")
#
#         UM_roles_and_per_filters.Click_actions_icon()
#         UM_roles_and_per_filters.Click_active_opt()
#         UM_roles_and_per_filters.Click_Activate_btn()
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
#         if "Role status changed successfully!" in toast_text:
#             self.logger.info(f"Role status changed to Active successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_active_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(f"Role status change to active failed | Toast: {toast_text}")
#             assert False, f"Role status change to active failed | Toast: {toast_text}"
#
# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.User_Management.Roles_and_Permission.filters import Roles_and_permission_filters
# from utilities.customlogger import LogGen
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
# test_data = get_test_data(excel_path, "Roles_and_permission_filters")
#
# @pytest.mark.order(3)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_RP_change_to_active(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_Roles_and_permission_filters(self, driver, data):
#
#         search_name = data["search_name"]
#         select_status = data["select_status"]
#         start_date = data["start_date"]
#         end_date = data["end_date"]
#
#         self.logger.info(
#             f"===== START TEST | Roles_and_permission_filters | search={search_name} ====="
#         )
#
#         # ---------------------------
#         # LOGIN (ONLY ONCE)
#         # ---------------------------
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#             self.logger.info("LOGIN SUCCESS | First iteration login completed")
#         else:
#             self.logger.info("LOGIN SKIPPED | Already logged in")
#
#         # ---------------------------
#         # NAVIGATION
#         # ---------------------------
#         self.logger.info("STEP 1 | Navigating to Roles & Permission module")
#
#         UM_roles_and_per_filters = Roles_and_permission_filters(driver)
#         UM_roles_and_per_filters.Click_Dashboard()
#         UM_roles_and_per_filters.Click_User_management()
#         UM_roles_and_per_filters.Click_roles_and_permission()
#
#         self.logger.info("STEP 2 | Applying filters")
#         UM_roles_and_per_filters.Enter_search_name_field(search_name)
#         UM_roles_and_per_filters.Choose_select_status(select_status)
#         UM_roles_and_per_filters.Click_filter_calender()
#         UM_roles_and_per_filters.select_date_range(start_date, end_date)
#
#         self.logger.info("STEP 3 | Searching product in table")
#
#         status = UM_roles_and_per_filters.search_product(search_name, "Inactive")
#
#         if not status:
#             take_screenshot(
#                 driver,
#                 test_name="Roles_and_permission_filter_failed",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission"
#             )
#             self.logger.error("FILTER FAILED | No data found or status mismatch after applying filters")
#             assert status, "FILTER FAILED | No data found or status mismatch after applying filters"
#
#         self.logger.info("FILTER SUCCESS | Records found in table")
#
#         # ---------------------------
#         # ACTION FLOW
#         # ---------------------------
#         self.logger.info("STEP 4 | Performing status change action")
#
#         UM_roles_and_per_filters.Click_actions_icon()
#         UM_roles_and_per_filters.Click_active_opt()
#         UM_roles_and_per_filters.Click_Activate_btn()
#
#         # ---------------------------
#         # TOAST VALIDATION
#         # ---------------------------
#         self.logger.info("STEP 5 | Waiting for toast message")
#
#         try:
#             toast_text = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             self.logger.info(f"TOAST RECEIVED | {toast_text}")
#
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             self.logger.error("TOAST ERROR | Toast not displayed within timeout")
#
#         # ---------------------------
#         # FINAL VALIDATION
#         # ---------------------------
#         if "Role status changed successfully!" in toast_text:
#             self.logger.info(
#                 f"TEST PASSED | Role changed to ACTIVE successfully | {toast_text}"
#             )
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_active_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(
#                 f"TEST FAILED | Role status change failed | Toast={toast_text}"
#             )
#             assert False, f"Role status change to active failed | Toast: {toast_text}"

import pytest
import time
from selenium.webdriver.common.by import By
from pages.User_Management.Roles_and_Permission.filters import Roles_and_permission_filters
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
test_data = get_test_data(excel_path, "Roles_and_permission_filters")

@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
class Test_UM_RP_change_to_active(BaseTest):

    logger = LogGen.loggen()

    def test_Roles_and_permission_filters(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== Roles And Permission Status Change Test Started | Search: {search_name} ====="
        )

        self.logger.info(
            f"Filter Details | "
            f"Search Name: {search_name} | "
            f"Status: {select_status} | "
            f"Start Date: {start_date} | "
            f"End Date: {end_date}"
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

        # =========================
        # NAVIGATION LOGS
        # =========================
        self.logger.info("Navigating to Dashboard")

        UM_roles_and_per_filters = Roles_and_permission_filters(driver)

        UM_roles_and_per_filters.Click_Dashboard()

        self.logger.info("Opening User Management module")

        UM_roles_and_per_filters.Click_User_management()

        self.logger.info("Opening Roles And Permission section")

        UM_roles_and_per_filters.Click_roles_and_permission()

        # =========================
        # FILTER LOGS
        # =========================
        self.logger.info("Applying roles and permission filters")

        UM_roles_and_per_filters.Enter_search_name_field(search_name)
        UM_roles_and_per_filters.Choose_select_status(select_status)
        UM_roles_and_per_filters.Click_filter_calender()
        UM_roles_and_per_filters.select_date_range(start_date, end_date)

        self.logger.info("Validating filtered table records")

        status = UM_roles_and_per_filters.search_product(search_name, "Inactive")

        if not status:

            self.logger.error(
                "Filter validation failed | No data found or status mismatch after applying filters"
            )

            take_screenshot(
                driver,
                test_name="Roles_and_permission_filter_failed",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )

            assert status, (
                "FILTER FAILED | No data found or status mismatch after applying filters"
            )

        self.logger.info(
            "Filter applied successfully | Records found in table"
        )

        # =========================
        # STATUS CHANGE LOGS
        # =========================
        self.logger.info(
            f"Changing role status to ACTIVE for: {search_name}"
        )

        UM_roles_and_per_filters.Click_actions_icon()
        UM_roles_and_per_filters.Click_active_opt()
        UM_roles_and_per_filters.Click_Activate_btn()

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

            print("Toast:", toast_text)

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error(
                "Toast message not displayed after role status update"
            )

        # =========================
        # VALIDATION LOGS
        # =========================
        if "Role status changed successfully!" in toast_text:

            self.logger.info(
                f"Role status changed to ACTIVE successfully | {toast_text}"
            )

        else:

            self.logger.error(
                f"Role status change FAILED | Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="UM_Role_status_active_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
            )

            assert False, (
                f"Role status change to active failed | Toast: {toast_text}"
            )