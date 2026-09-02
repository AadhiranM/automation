import time

import pytest
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.UserManagement.sa_user_list_page import (
    SAUserListPage
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestUserListNegative:

    # =========================================================
    # INVALID SEARCH
    # =========================================================

    def test_search_invalid_user(self, setup):

        page = SAUserListPage(setup)

        page.goto_page()

        print("=" * 60)
        print("NEGATIVE USER SEARCH TEST")
        print("=" * 60)

        invalid_user = "INVALID_USER_999999"

        print(
            f"Searching invalid user: {invalid_user}"
        )

        page.type(
            page.SEARCH_BOX,
            invalid_user
        )

        page.click(
            page.SEARCH_BTN
        )

        print(
            "Search button clicked"
        )

        page.wait_for_results()

        assert page.has_no_data(), (
            "No Result Found was not displayed "
            f"for invalid user: {invalid_user}"
        )

        print(
            f"PASS: {invalid_user} "
            "-> No Result Found"
        )

    # =========================================================
    # INVALID DATE RANGE
    #
    # Current year:
    # 2026
    #
    # YEAR DOWN:
    # 2026 -> 2025 -> 2024
    #
    # MONTH:
    # September -> January
    #
    # DATE:
    # 01 Jan 2024 -> 02 Jan 2024
    # =========================================================

    def test_filter_invalid_date_range(self, setup):

        page = SAUserListPage(setup)

        page.goto_page()

        print("=" * 60)
        print("NEGATIVE USER DATE FILTER TEST")
        print("=" * 60)

        # --------------------------------------------------
        # Open Created At date picker
        # --------------------------------------------------

        date_filter = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@type='text' "
                    "and @placeholder='Filter by : Created At']"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            date_filter
        )

        print("Date picker opened")

        wait = WebDriverWait(
            page.driver,
            10
        )

        # --------------------------------------------------
        # Current year
        #
        # 2026 -> 2025 -> 2024
        # --------------------------------------------------

        year_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//input[contains(@class,'numInput')]"
                )
            )
        )

        current_year = int(
            year_input.get_attribute("value")
        )

        print(
            f"Current calendar year: {current_year}"
        )

        target_year = 2024

        # --------------------------------------------------
        # Click YEAR DOWN arrow only
        # --------------------------------------------------

        while current_year > target_year:

            year_down = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class,'flatpickr-calendar') "
                        "and contains(@class,'open')]"
                        "//span[contains(@class,'arrowDown')]"
                    )
                )
            )

            page.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                year_down
            )

            page.driver.execute_script(
                "arguments[0].click();",
                year_down
            )

            time.sleep(0.5)

            year_input = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'flatpickr-calendar') "
                        "and contains(@class,'open')]"
                        "//input[contains(@class,'numInput')]"
                    )
                )
            )

            current_year = int(
                year_input.get_attribute("value")
            )

            print(
                f"Year after DOWN arrow: {current_year}"
            )

        # --------------------------------------------------
        # Verify 2024
        # --------------------------------------------------

        assert current_year == 2024, (
            f"Year navigation failed. "
            f"Expected 2024, "
            f"Actual {current_year}"
        )

        print(
            "Year successfully changed: "
            "2026 -> 2025 -> 2024"
        )

        # --------------------------------------------------
        # Change MONTH
        #
        # September 2024 -> January 2024
        # --------------------------------------------------

        month_dropdown = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//select[contains("
                    "@class,"
                    "'flatpickr-monthDropdown-months'"
                    ")]"
                )
            )
        )

        print(
            "Month dropdown found"
        )

        Select(
            month_dropdown
        ).select_by_visible_text(
            "January"
        )

        print(
            "Month successfully changed to January"
        )

        # --------------------------------------------------
        # Verify January
        # --------------------------------------------------

        wait.until(
            lambda d:
            d.find_element(
                By.XPATH,
                "//div[contains(@class,'flatpickr-calendar') "
                "and contains(@class,'open')]"
                "//select[contains("
                "@class,"
                "'flatpickr-monthDropdown-months'"
                ")]"
            ).get_attribute("value") == "0"
        )

        print(
            "Calendar is now showing January 2024"
        )

        # --------------------------------------------------
        # Select January 1, 2024
        # --------------------------------------------------

        jan_1 = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//span[contains(@class,'flatpickr-day') "
                    "and @aria-label='January 1, 2024']"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_1
        )

        print(
            "Selected: 01 Jan 2024"
        )

        # --------------------------------------------------
        # Select January 2, 2024
        # --------------------------------------------------

        jan_2 = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//span[contains(@class,'flatpickr-day') "
                    "and @aria-label='January 2, 2024']"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_2
        )

        print(
            "Selected: 02 Jan 2024"
        )

        # --------------------------------------------------
        # Date range is automatically applied after
        # selecting the END date.
        # --------------------------------------------------

        print(
            "Date range selected successfully"
        )

        # --------------------------------------------------
        # Wait for No Result Found
        # --------------------------------------------------

        wait.until(
            lambda d: page.has_no_data()
        )

        assert page.has_no_data(), (
            "No Result Found was not displayed "
            "for invalid date range: "
            "01 Jan 2024 - 02 Jan 2024"
        )

        print(
            "PASS: 01 Jan 2024 - 02 Jan 2024 "
            "-> No Result Found"
        )

        # --------------------------------------------------
        # Wait for No Result Found
        # --------------------------------------------------

        wait.until(
            lambda d: page.has_no_data()
        )

        assert page.has_no_data(), (
            "No Result Found was not displayed "
            "for invalid date range: "
            "01 Jan 2024 - 02 Jan 2024"
        )

        print(
            "PASS: 01 Jan 2024 - 02 Jan 2024 "
            "-> No Result Found"
        )