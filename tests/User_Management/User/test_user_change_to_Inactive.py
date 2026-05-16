# import pytest
# import time
# from selenium.webdriver.common.by import By
#
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.User_Management.Users.user_filters import user_filters
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
#
# # ---------------------------
# # LOAD EXCEL DATA
# # ---------------------------
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "user_filters")
#
# @pytest.mark.order(3)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_users_change_to_Inactive(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_UM_users_change_to_Inactive(self, driver, data):
#
#         search_name = data["search_name"]
#         select_status = data["select_status"]
#         start_date = data["start_date"]
#         end_date = data["end_date"]
#
#         self.logger.info(
#             f"===== User_management_user_filters ====="
#         )
#         # ---------------------------
#
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
#         UM_user_filters = user_filters(driver)
#         UM_user_filters.Click_Dashboard()
#         UM_user_filters.Click_User_management()
#         UM_user_filters.Click_users()
#         UM_user_filters.Enter_search_field(search_name)
#         UM_user_filters.Choose_select_status(select_status)
#         UM_user_filters.Click_filter_calender()
#         UM_user_filters.select_date_range(start_date,end_date)
#
#         status =UM_user_filters.search_product(search_name)  # True if rows exist
#
#         if not status:
#             take_screenshot(
#                 driver,
#                 test_name="user_filter_failed",
#                 folder_name="Screenshots\\User_Management\\Users\\filter"
#             )
#             self.logger.error("Filter validation failed | No data found or status mismatch after applying filters")
#             assert status, "Filter failed | No data found or status mismatch after applying filters"
#         self.logger.info("Filter applied successfully, table has records")
#         time.sleep(2)
#
#         UM_user_filters.Click_actions_icon()
#         UM_user_filters.Click_suspend_opt()
#         UM_user_filters.Click_suspend_btn()
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
#         if "User status changed successfully!" in toast_text:
#             self.logger.info(f"Role status changed to Inactive successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_inactive_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(f"User status change to Inactive failed | Toast: {toast_text}")
#             assert False, f"User status change to Inactive failed | Toast: {toast_text}"
#



import pytest
import time
from selenium.webdriver.common.by import By

from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.User_Management.Users.user_filters import user_filters
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
test_data = get_test_data(excel_path, "user_filters")


@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
class Test_UM_users_change_to_Inactive(BaseTest):

    logger = LogGen.loggen()

    def test_UM_users_change_to_Inactive(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== User Management | Users | Change Status To INACTIVE | Search={search_name} ====="
        )

        self.logger.info(
            f"Filter Details | Search: {search_name} | "
            f"Status: {select_status} | "
            f"Start Date: {start_date} | End Date: {end_date}"
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

        UM_user_filters = user_filters(driver)

        UM_user_filters.Click_Dashboard()

        self.logger.info("Opening User Management module")
        UM_user_filters.Click_User_management()

        self.logger.info("Opening Users page")
        UM_user_filters.Click_users()

        # =========================
        # FILTER LOGS
        # =========================
        self.logger.info("Applying user filters")

        UM_user_filters.Enter_search_field(search_name)
        UM_user_filters.Choose_select_status(select_status)

        self.logger.info("Opening calendar filter")
        UM_user_filters.Click_filter_calender()

        self.logger.info(
            f"Selecting date range | From: {start_date} | To: {end_date}"
        )

        UM_user_filters.select_date_range(start_date, end_date)

        self.logger.info("Searching filtered records in table")

        status = UM_user_filters.search_product(search_name,"Active")

        # =========================
        # FILTER VALIDATION
        # =========================
        if not status:

            take_screenshot(
                driver,
                test_name="user_filter_failed",
                folder_name="Screenshots\\User_Management\\Users\\filter"
            )

            self.logger.error(
                "Filter validation failed | "
                "No data found or status mismatch after applying filters"
            )

            assert status, (
                "Filter failed | "
                "No data found or status mismatch after applying filters"
            )

        self.logger.info(
            "Filter validation successful | Records found in table"
        )

        time.sleep(2)

        # =========================
        # STATUS CHANGE ACTION
        # =========================
        self.logger.info("Opening Actions menu")

        UM_user_filters.Click_actions_icon()

        self.logger.info("Selecting Suspend / Inactive option")

        UM_user_filters.Click_suspend_opt()

        self.logger.info("Confirming Inactive status change")

        UM_user_filters.Click_suspend_btn()

        # =========================
        # TOAST VALIDATION
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
                "Toast validation failed | Toast message not displayed"
            )

        # =========================
        # FINAL VALIDATION
        # =========================
        if "User status changed successfully!" in toast_text:

            self.logger.info(
                f"User status changed to INACTIVE successfully | {toast_text}"
            )

        else:

            take_screenshot(
                driver,
                test_name="UM_Role_status_inactive_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
            )

            self.logger.error(
                f"User status change to INACTIVE failed | Toast: {toast_text}"
            )

            assert False, (
                f"User status change to Inactive failed | Toast: {toast_text}"
            )