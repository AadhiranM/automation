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
class Test_UM_RP_filters(BaseTest):

    logger = LogGen.loggen()

    def test_Roles_and_permission_filters(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        self.logger.info(
            f"===== Roles_and_permission_filters ====="
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
        UM_roles_and_per_filters = Roles_and_permission_filters(driver)
        UM_roles_and_per_filters.Click_Dashboard()
        UM_roles_and_per_filters.Click_User_management()
        UM_roles_and_per_filters.Click_roles_and_permission()
        UM_roles_and_per_filters.Enter_search_name_field(search_name)
        UM_roles_and_per_filters.Choose_select_status(select_status)
        UM_roles_and_per_filters.Click_filter_calender()
        UM_roles_and_per_filters.select_date_range(start_date,end_date)
        status =UM_roles_and_per_filters.search_product(search_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="Roles_and_permission_filter_failed",
                folder_name="Screenshots\\User_Management\\Roles_and_permission"
            )
            self.logger.error("Filter applied but no records found in table")
            assert status, "No rows found after applying filters!"
        self.logger.info("Filter applied successfully, table has records")
        UM_roles_and_per_filters.Click_actions_icon()

        try:
            UM_roles_and_per_filters.Click_Inactive_opt()
            UM_roles_and_per_filters.Click_suspend_btn()
            try:
                toast_text = WebDriverWait(driver,3).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".toastify")
                    )
                ).text
                if toast_text:
                    print("Toast:", toast_text)

                # validation
                if toast_text and "Role status changed successfully!" in toast_text:
                    self.logger.info("Role status changed to Inactive successfully")

            except TimeoutException:
                take_screenshot(
                    driver,
                    test_name="UM_Role_status_fail",
                    folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
                )
                self.logger.error(f"Role status change to Inactive failed")
                assert False, "Role status change to Inactive failed"

        except:
            UM_roles_and_per_filters.Click_active_opt()
            UM_roles_and_per_filters.Click_Activate_btn()
            try:
                toast_text = WebDriverWait(driver,3).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".toastify")
                    )
                ).text
                if toast_text:
                    print("Toast:", toast_text)

                # validation
                if toast_text and "Role status changed to Active successfully!" in toast_text:
                    self.logger.info("Role status changed to Active successfully")

            except TimeoutException:
                take_screenshot(
                    driver,
                    test_name="UM_Role_status_fail",
                    folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
                )
                self.logger.error(f"Role status change to active failed")
                assert False, "Role status change to active failed"






