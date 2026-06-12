# import pytest
# import time
# from selenium.webdriver.common.by import By
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
# # ---------------------------
# # LOAD EXCEL DATA
# # ---------------------------
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "user_filters")
#
# @pytest.mark.order(2)
# @pytest.mark.parametrize("data", test_data)
# class Test_UM_users_change_to_active(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_UM_users_change_to_active(self, driver, data):
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
#         status=UM_user_filters.search_product(search_name)  # True if rows exist
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
#         UM_user_filters.Click_activate_opt()
#         UM_user_filters.Click_Activate_btn()
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
#             self.logger.info(f"User status changed to Active successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="UM_Role_status_active_fail",
#                 folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
#             )
#             self.logger.error(f"User status change to active failed | Toast: {toast_text}")
#             assert False, f"User status change to active failed | Toast: {toast_text}"


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


@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_UM_users_change_to_active(BaseTest):

    logger = LogGen.loggen()

    def test_UM_users_change_to_active(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== User Status Change To Active Test Started | User: {search_name} ====="
        )

        self.logger.info(
            f"Filter Details | Search: {search_name} | Status: {select_status} | "
            f"Start Date: {start_date} | End Date: {end_date}"
        )

        # ---------------------------
        # LOGIN (ONLY ONCE)
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

        self.logger.info("Opening filter calendar")
        UM_user_filters.Click_filter_calender()

        self.logger.info(
            f"Selecting date range | Start: {start_date} | End: {end_date}"
        )

        UM_user_filters.select_date_range(start_date, end_date)

        # =========================
        # SEARCH VALIDATION
        # =========================
        self.logger.info("Searching filtered user in table")

        status = UM_user_filters.search_product(search_name,"Suspended")

        if not status:

            self.logger.error(
                "No matching records found after applying filters"
            )

            take_screenshot(
                driver,
                test_name="user_filter_failed",
                folder_name="Screenshots\\User_Management\\Users\\filter"
            )

            assert status, (
                "Filter failed | No data found or status mismatch after applying filters"
            )

        self.logger.info("Filtered records found successfully")

        time.sleep(1)

        # =========================
        # ACTION LOGS
        # =========================
        self.logger.info("Opening actions menu")

        UM_user_filters.Click_actions_icon()

        self.logger.info("Selecting Activate option")
        UM_user_filters.Click_activate_opt()

        self.logger.info("Confirming Activate action")
        UM_user_filters.Click_Activate_btn()

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
        if "User status changed successfully!" in toast_text:

            self.logger.info(
                f"User status changed to ACTIVE successfully | {toast_text}"
            )

        else:

            self.logger.error(
                f"User status change to ACTIVE failed | Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="UM_Role_status_active_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
            )

            assert False, (
                f"User status change to active failed | Toast: {toast_text}"
            )


