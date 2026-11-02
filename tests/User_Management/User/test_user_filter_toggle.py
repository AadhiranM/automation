import pytest
import time
from selenium.webdriver.common.by import By
from pages.User_Management.Users.user_filters import user_filters
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.read_excel import get_test_data
import random
import string
from datetime import datetime, timedelta

@pytest.mark.order(4)
class Test_UM_user_filter_toggle(BaseTest):

    logger = LogGen.loggen()

    def test_UM_user_filter_toggle(self, driver):

        self.logger.info(
            "===== User Management | Users | Filter Toggle Test Started ====="
        )

        wait = WebDriverWait(driver, 10)

        # =========================
        # NAVIGATION
        # =========================
        self.logger.info("Refreshing the application")
        driver.refresh()

        self.logger.info("Navigating to Dashboard")
        UM_user_filters = user_filters(driver)
        UM_user_filters.Click_Dashboard()

        self.logger.info("Opening User Management module")
        UM_user_filters.Click_User_management()

        self.logger.info("Opening Users page")
        UM_user_filters.Click_users()

        time.sleep(2)

        self.logger.info("Successfully navigated to Users page")

        # =========================
        # FETCH VALUES FROM FIRST TABLE ROW
        # =========================
        self.logger.info("Fetching filter values from the first table row")

        search_name_locator = (By.XPATH, "//tbody/tr[1]/td[2]")

        created_by = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[9]//span[@class='avatar-text copy-ellipsis-text']")
            )
        ).text.strip()

        self.logger.info(f"Fetched Created By: {created_by}")

        name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_name_locator)
        ).text.strip()

        self.logger.info(f"Fetched User Name: {name}")

        role = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[4]")
            )
        ).text.strip()

        self.logger.info(f"Fetched User Role: {role}")

        user_type = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[6]")
            )
        ).text.strip()

        self.logger.info(f"Fetched User Type: {user_type}")

        # =========================
        # APPLY FILTERS
        # =========================
        time.sleep(2)

        self.logger.info("Opening Filter Toggle")
        UM_user_filters.Click_filter_toggle()

        self.logger.info(f"Entering User Name in filter: {name}")
        UM_user_filters.Enter_filter_toggle_name(name)

        # self.logger.info("Selecting Created By filter")
        # UM_user_filters.Click_filter_toggle_created_by_opt()
        # UM_user_filters.Enter_filter_toggle_created_by_field(created_by)

        # self.logger.info("Selecting Role filter")
        # UM_user_filters.Click_filter_toggle_role_opt()
        # UM_user_filters.Enter_filter_toggle_role_field(role)

        # self.logger.info("Selecting User Type filter")
        # UM_user_filters.Click_filter_toggle_user_type_opt()
        # UM_user_filters.Enter_filter_toggle_user_type_field(user_type)

        self.logger.info("Clicking Apply button")
        UM_user_filters.Click_filter_toggle_apply_btn()

        self.logger.info("Filter applied successfully")
        time.sleep(2)

        # =========================
        # CHANGE USER STATUS
        # =========================
        self.logger.info("Opening Actions menu")
        UM_user_filters.Click_actions_icon()

        wait = WebDriverWait(driver, 10)

        try:
            self.logger.info("Checking whether Suspend option is available")

            suspend_option = wait.until(
                EC.visibility_of_element_located(
                    UM_user_filters.suspend_opt
                )
            )

            if suspend_option.is_displayed():
                self.logger.info(
                    "User is Active. Selecting Suspend option"
                )

                UM_user_filters.Click_suspend_opt()

                self.logger.info("Clicking Yes to confirm Suspend action")
                UM_user_filters.Click_yes_btn()

                self.logger.info("Suspend confirmation submitted")

        except TimeoutException:

            self.logger.info(
                "Suspend option not available. Checking Activate option"
            )

            UM_user_filters.Click_activate_opt()

            self.logger.info("Clicking Yes to confirm Activate action")
            UM_user_filters.Click_yes_btn()

            self.logger.info("Activate confirmation submitted")

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

            toast_text = toast_text.encode(
                "ascii", errors="ignore"
            ).decode().strip()

            print("Toast:", toast_text)

            self.logger.info(f"Toast received: {toast_text}")

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
                f"User status changed successfully | {toast_text}"
            )

        else:

            self.logger.error(
                f"User status change failed | Toast: {toast_text}"
            )

            self.logger.info("Taking screenshot for failure analysis")

            take_screenshot(
                driver,
                test_name="UM_user_status_change_fail",
                folder_name="Screenshots\\User_Management\\Users\\filter"
            )

            assert False, (
                f"User status change failed | Toast: {toast_text}"
            )

        self.logger.info(
            "===== User Management | Users | Filter Toggle Test Completed Successfully ====="
        )