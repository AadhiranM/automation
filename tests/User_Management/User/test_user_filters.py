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

@pytest.mark.order(2)
class Test_UM_user_filters(BaseTest):

    logger = LogGen.loggen()

    def test_UM_user_filter(self, driver):

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            "===== User Management | Users | Filter Test Started ====="
        )
        wait = WebDriverWait(driver, 10)
        # =========================
        # NAVIGATION
        # =========================
        driver.refresh()
        self.logger.info("Navigating to Dashboard")

        UM_user_filters = user_filters(driver)

        UM_user_filters.Click_Dashboard()

        self.logger.info("Opening User Management module")
        UM_user_filters.Click_User_management()

        self.logger.info("Opening Users page")
        UM_user_filters.Click_users()
        time.sleep(3)

        # =========================
        # FETCH VALUES FROM FIRST TABLE ROW
        # =========================
        self.logger.info("Fetching filter values from the first table row")

        search_name_locator = (By.XPATH, "//tbody/tr[1]/td[2]")

        search_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_name_locator)
        ).text.strip()

        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[10]")
            )
        ).text.strip()

        actual_date = datetime.strptime(
            date_value, "%d %b %Y, %I:%M %p"
        )
        start_date = (
                actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        print("Search Value:", search_name)
        print("Start Date:", start_date)
        print("End Date:", end_date)

        self.logger.info(f"Search Value: {search_name}")
        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")

        self.logger.info(f"Search Name fetched: {search_name}")


        # =========================
        # APPLY FILTERS
        # =========================
        self.logger.info("Applying user filters")

        UM_user_filters.Enter_search_field(search_name)

        select_status = "All"
        UM_user_filters.Choose_select_status(select_status)
        self.logger.info(f"Selected Status: {select_status}")

        UM_user_filters.Click_filter_calender()
        self.logger.info("Opened calendar filter")

        UM_user_filters.select_date_range(start_date, end_date)
        self.logger.info(
            f"Selected Date Range | Start Date: {start_date} | "
            f"End Date: {end_date}"
        )


        self.logger.info("Searching filtered records in table")


        time.sleep(2)

        self.logger.info("Opening Actions menu")
        UM_user_filters.Click_actions_icon()

        wait = WebDriverWait(driver, 10)

        try:
            suspend_option = wait.until(
                EC.visibility_of_element_located(
                    UM_user_filters.suspend_opt
                )
            )

            if suspend_option.is_displayed():
                self.logger.info("User is Active. Selecting Suspend option")
                UM_user_filters.Click_suspend_opt()
                UM_user_filters.Click_yes_btn()

        except TimeoutException:

            self.logger.info("Checking Activate option")
            UM_user_filters.Click_activate_opt()
            UM_user_filters.Click_yes_btn()
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
                f"User status changed successfully | {toast_text}"
            )

        else:
            take_screenshot(
                driver,
                test_name="UM_user_status_change_fail",
                folder_name="Screenshots\\User_Management\\Users\\filter"
            )

            self.logger.error(
                f"User status change failed | Toast: {toast_text}"
            )

            assert False, (
                f"User status change failed | Toast: {toast_text}"
            )
        self.logger.info(
            "===== User Management | Users | Filter Test Completed ====="
        )