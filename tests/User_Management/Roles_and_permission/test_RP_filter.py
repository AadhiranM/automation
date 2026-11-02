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
from datetime import datetime, timedelta


@pytest.mark.order(2)
class Test_RP_filters(BaseTest):

    logger = LogGen.loggen()

    def test_RP_filters(self, driver):

        # LOGGER START
        # =========================
        self.logger.info("===== Roles And Permission filter Test Started =====")

        wait = WebDriverWait(driver, 10)

        # NAVIGATION
        # =========================
        self.logger.info("Navigating to Dashboard")

        UM_roles_and_per_filters = Roles_and_permission_filters(driver)
        UM_roles_and_per_filters.Click_Dashboard()

        self.logger.info("Dashboard opened successfully")

        self.logger.info("Opening User Management module")
        UM_roles_and_per_filters.Click_User_management()

        self.logger.info("User Management module opened successfully")

        self.logger.info("Opening Roles And Permission section")
        UM_roles_and_per_filters.Click_roles_and_permission()

        self.logger.info("Roles And Permission page opened successfully")

        # FILTER LOGS
        # =========================
        self.logger.info("Starting Roles And Permission filter validation")

        role_name_locator = (By.XPATH, "//tbody/tr[1]/td[2]")
        created_at_locator = (By.XPATH, "//tbody/tr[1]/td[7]")
        select_status = "All"

        self.logger.info("Fetching role name from the first table row")

        role_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(role_name_locator)
        ).text.strip()

        self.logger.info(f"Role name fetched successfully: {role_name}")

        self.logger.info("Fetching Created At date from the first table row")

        date_value = wait.until(
            EC.visibility_of_element_located(created_at_locator)
        ).text.strip()

        self.logger.info(f"Created At date fetched: {date_value}")

        actual_date = datetime.strptime(
            date_value, "%d %b %Y %I:%M %p"
        )

        start_date = (
            actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        self.logger.info(f"Search Value: {role_name}")
        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")
        self.logger.info(f"Selected Status: {select_status}")

        print("Search Value:", role_name)
        print("Start Date:", start_date)
        print("End Date:", end_date)

        self.logger.info("Entering role name in search field")
        UM_roles_and_per_filters.Enter_search_name_field(role_name)

        self.logger.info("Selecting status filter")
        UM_roles_and_per_filters.Choose_select_status(select_status)

        self.logger.info("Opening date range calendar")
        UM_roles_and_per_filters.Click_filter_calender()

        self.logger.info("Applying date range filter")
        UM_roles_and_per_filters.select_date_range(start_date, end_date)

        self.logger.info("Date range filter applied successfully")

        time.sleep(3)

        self.logger.info("Roles And Permission filters applied successfully")

        # STATUS UPDATE
        # =========================
        self.logger.info("Starting role status update validation")

        self.logger.info("Opening Actions menu")
        UM_roles_and_per_filters.Click_actions_icon()

        self.logger.info("Actions menu opened successfully")

        try:
            self.logger.info("Checking Activate option")

            activate_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    UM_roles_and_per_filters.active_opt
                )
            )

            self.logger.info("Activate option is available")

            activate_option.click()

            self.logger.info("Activate option clicked successfully")

            self.logger.info("Clicking Yes button to confirm status update")
            UM_roles_and_per_filters.Click_yes_btn()

            self.logger.info("Status update confirmation submitted")

        except TimeoutException:

            self.logger.info("Activate option not found")

            self.logger.info("Checking Inactivate option")

            deactivate_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    UM_roles_and_per_filters.inactive_opt
                )
            )

            self.logger.info("Inactivate option is available")

            deactivate_option.click()

            self.logger.info("Inactivate option clicked successfully")

            self.logger.info("Clicking Yes button to confirm status update")
            UM_roles_and_per_filters.Click_yes_btn()

            self.logger.info("Status update confirmation submitted")

        # TOAST HANDLING
        # =========================
        self.logger.info("Waiting for toast response")

        try:
            toast_text = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text.strip()

            toast_text = toast_text.encode(
                "ascii", errors="ignore"
            ).decode()

            print("Toast:", toast_text)

            self.logger.info(f"Toast message received: {toast_text}")

        except TimeoutException:

            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error(
                "Toast message not displayed after role status update"
            )

        # VALIDATION LOGS
        # =========================
        self.logger.info("Validating role status update response")

        if "Role status changed successfully!" in toast_text:

            self.logger.info(
                f"Role status changed successfully | {toast_text}"
            )

        else:

            self.logger.error(
                f"Role status change FAILED | Toast: {toast_text}"
            )

            self.logger.info("Capturing screenshot for failed status update")

            take_screenshot(
                driver,
                test_name="UM_Role_status_fail",
                folder_name="Screenshots\\User_Management\\Roles_and_permission\\filters"
            )

            self.logger.info("Failure screenshot captured")

            assert False, (
                f"Role status change failed | Toast: {toast_text}"
            )

        self.logger.info("===== Roles And Permission filter Test Completed =====")