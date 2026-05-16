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
# @pytest.mark.order(2)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_RP_change_to_Inactive(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_UM_RP_change_to_Inactive(self, driver, data):
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
#         status =UM_roles_and_per_filters.search_product(search_name,"Active")  # True if rows exist
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
#         UM_roles_and_per_filters.Click_actions_icon()
#
#         UM_roles_and_per_filters.Click_Inactive_opt()
#         UM_roles_and_per_filters.Click_suspend_btn()
#         try:
#             toast_text = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             print("Toast:", toast_text)
#         # VALIDATION
#         if "Role status changed successfully!" in toast_text:
#             self.logger.info(f"Role status changed to Inactive successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_inactive_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(f"Role status change to Inactive failed | Toast: {toast_text}")
#             assert False, f"Role status change to Inactive failed | Toast: {toast_text}"
#
#
#
#

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
# @pytest.mark.order(2)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_RP_change_to_Inactive(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_UM_RP_change_to_Inactive(self, driver, data):
#
#         search_name = data["search_name"]
#         select_status = data["select_status"]
#         start_date = data["start_date"]
#         end_date = data["end_date"]
#
#         # ---------------------------
#         # START
#         # ---------------------------
#         self.logger.info(
#             f"===== START TEST | Roles_and_permission_filters | ACTION=INACTIVE | SEARCH={search_name} ====="
#         )
#
#         # ---------------------------
#         # LOGIN
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
#         self.logger.info("STEP 1 | Navigating to Dashboard")
#
#         UM_roles_and_per_filters = Roles_and_permission_filters(driver)
#         UM_roles_and_per_filters.Click_Dashboard()
#
#         self.logger.info("STEP 2 | Navigating to User Management")
#         UM_roles_and_per_filters.Click_User_management()
#
#         self.logger.info("STEP 3 | Opening Roles & Permission page")
#         UM_roles_and_per_filters.Click_roles_and_permission()
#
#         # ---------------------------
#         # FILTER ACTION
#         # ---------------------------
#         self.logger.info("STEP 4 | Applying filters")
#
#         UM_roles_and_per_filters.Enter_search_name_field(search_name)
#         UM_roles_and_per_filters.Choose_select_status(select_status)
#         UM_roles_and_per_filters.Click_filter_calender()
#         UM_roles_and_per_filters.select_date_range(start_date, end_date)
#
#         self.logger.info("STEP 5 | Searching record in table")
#
#         status = UM_roles_and_per_filters.search_product(search_name, "Active")
#
#         if not status:
#             take_screenshot(
#                 driver,
#                 test_name="Roles_and_permission_filter_failed",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission"
#             )
#             self.logger.error("FILTER FAILED | Either No data or status mismatch after applying filters")
#             assert status, "FILTER FAILED | No data found or status mismatch after applying filters"
#
#         self.logger.info("FILTER SUCCESS | Record found in table")
#
#         # ---------------------------
#         # ACTION
#         # ---------------------------
#         self.logger.info("STEP 6 | Performing status change to INACTIVE")
#
#         UM_roles_and_per_filters.Click_actions_icon()
#         UM_roles_and_per_filters.Click_Inactive_opt()
#         UM_roles_and_per_filters.Click_suspend_btn()
#
#         # ---------------------------
#         # TOAST
#         # ---------------------------
#         self.logger.info("STEP 7 | Waiting for toast message")
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
#         # VALIDATION
#         # ---------------------------
#         if "Role status changed successfully!" in toast_text:
#             self.logger.info(
#                 f"TEST PASSED | Role changed to INACTIVE successfully | {toast_text}"
#             )
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_inactive_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(
#                 f"TEST FAILED | Role change to INACTIVE failed | Toast={toast_text}"
#             )
#             assert False, f"Role status change to Inactive failed | Toast: {toast_text}"


import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.User_Management.Roles_and_Permission.filters import Roles_and_permission_filters
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
test_data = get_test_data(excel_path, "Roles_and_permission_filters")


@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_UM_RP_change_to_Inactive(BaseTest):

    logger = LogGen.loggen()

    def test_UM_RP_change_to_Inactive(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== Roles & Permission Change To Inactive Test Started | Search: {search_name} ====="
        )

        self.logger.info(
            f"Filter Details | Search: {search_name} | Status: {select_status} | "
            f"Start Date: {start_date} | End Date: {end_date}"
        )

        # ---------------------------
        # LOGIN
        # ---------------------------
        if data == test_data[0]:

            self.logger.info("Executing login flow for first iteration")

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

        self.logger.info("Opening Roles & Permission page")
        UM_roles_and_per_filters.Click_roles_and_permission()

        # =========================
        # FILTER LOGS
        # =========================
        self.logger.info("Applying filters")

        UM_roles_and_per_filters.Enter_search_name_field(search_name)
        UM_roles_and_per_filters.Choose_select_status(select_status)

        self.logger.info("Opening filter calendar")
        UM_roles_and_per_filters.Click_filter_calender()

        self.logger.info(
            f"Selecting date range | Start: {start_date} | End: {end_date}"
        )

        UM_roles_and_per_filters.select_date_range(start_date, end_date)

        # =========================
        # SEARCH VALIDATION
        # =========================
        self.logger.info("Searching filtered record in table")

        status = UM_roles_and_per_filters.search_product(search_name, "Active")

        if not status:

            self.logger.error(
                "Filter failed | No matching or status mismatch after applying filters"
            )

            take_screenshot(
                driver,
                test_name="Roles_and_permission_filter_failed",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )

            assert status, (
                "filter failed |No data found or status mismatch after applying filters!"
            )

        self.logger.info("Filtered records found successfully")

        # =========================
        # ACTION LOGS
        # =========================
        self.logger.info("Opening actions menu")

        UM_roles_and_per_filters.Click_actions_icon()

        self.logger.info("Selecting Inactive option")
        UM_roles_and_per_filters.Click_Inactive_opt()

        self.logger.info("Confirming suspend action")
        UM_roles_and_per_filters.Click_suspend_btn()

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
        if "Role status changed successfully!" in toast_text:

            self.logger.info(
                f"Role status changed to INACTIVE successfully | {toast_text}"
            )

        else:

            self.logger.error(
                f"Role status change to INACTIVE failed | Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="UM_Role_status_inactive_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
            )

            assert False, (
                f"Role status change to Inactive failed | Toast: {toast_text}"
            )
