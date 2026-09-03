import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from pages.superadmin.Applicationusers.sa_application_user_page import (
    SAApplicationUserPage
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestApplicationUsersNegative:

    # =========================================================
    # INVALID SEARCH
    # =========================================================

    def test_search_invalid_user(self, setup):

        page = SAApplicationUserPage(setup)

        page.goto_page()

        wait = WebDriverWait(
            page.driver,
            20,
            poll_frequency=0.5,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        )

        print("=" * 60)
        print("NEGATIVE APPLICATION USER SEARCH TEST")
        print("=" * 60)

        invalid_id = "999999999999"

        search_box = wait.until(
            EC.visibility_of_element_located(
                page.SEARCH_BOX
            )
        )

        search_box.clear()
        search_box.send_keys(invalid_id)

        print(
            f"Invalid ID entered: {invalid_id}"
        )

        search_button = wait.until(
            EC.element_to_be_clickable(
                page.SEARCH_BTN
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            search_button
        )

        print("Search button clicked")

        # Application Users refreshes the table asynchronously.
        wait.until(
            lambda d: page.has_no_data()
        )

        assert page.has_no_data(), (
            "No Result Found message was not displayed "
            f"for invalid ID: {invalid_id}"
        )

        print(
            f"PASS: Invalid ID {invalid_id} "
            "-> No Result Found"
        )

    # =========================================================
    # INVALID DATE RANGE
    #
    # IMPORTANT:
    # Application Users DOES NOT need the separate Filter button
    # after selecting the date range.
    #
    # The existing page object's filter_by_date() also confirms
    # that selecting the Flatpickr range is enough and then waits
    # for the result refresh.
    #
    # Here we manually navigate the Flatpickr year:
    #
    # 2026 -> 2025 -> 2024
    #
    # Then:
    # January 1, 2024
    # January 2, 2024
    #
    # After the second date is selected, the application itself
    # applies the filter / updates the URL.
    # =========================================================

    def test_filter_invalid_date_range(self, setup):

        page = SAApplicationUserPage(setup)

        page.goto_page()

        wait = WebDriverWait(
            page.driver,
            20,
            poll_frequency=0.5,
            ignored_exceptions=(
                StaleElementReferenceException,
            )
        )

        print("=" * 60)
        print("NEGATIVE APPLICATION USER DATE FILTER TEST")
        print("=" * 60)

        # ---------------------------------------------------------
        # Open date picker
        # ---------------------------------------------------------

        date_filter = wait.until(
            EC.element_to_be_clickable(
                page.DATE_FILTER
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            date_filter
        )

        print("Date picker opened")

        # ---------------------------------------------------------
        # Flatpickr locators
        # ---------------------------------------------------------

        calendar = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
        )

        year_input_locator = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
            "//input[contains(@class,'numInput')]"
        )

        year_down_locator = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
            "//span[contains(@class,'arrowDown')]"
        )

        month_dropdown_locator = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
            "//select[contains(@class,"
            "'flatpickr-monthDropdown-months')]"
        )

        # ---------------------------------------------------------
        # Read current year
        # ---------------------------------------------------------

        year_input = wait.until(
            EC.visibility_of_element_located(
                year_input_locator
            )
        )

        current_year = int(
            year_input.get_attribute("value")
        )

        print(
            f"Current calendar year: {current_year}"
        )

        target_year = 2024

        # ---------------------------------------------------------
        # YEAR DOWN ONLY
        #
        # Do NOT use previous-month arrow.
        # ---------------------------------------------------------

        while current_year > target_year:

            year_down = wait.until(
                EC.element_to_be_clickable(
                    year_down_locator
                )
            )

            page.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                year_down
            )

            # Re-find immediately before clicking because
            # Flatpickr can re-render after each year change.
            year_down = wait.until(
                EC.element_to_be_clickable(
                    year_down_locator
                )
            )

            page.driver.execute_script(
                "arguments[0].click();",
                year_down
            )

            time.sleep(0.5)

            year_input = wait.until(
                EC.visibility_of_element_located(
                    year_input_locator
                )
            )

            current_year = int(
                year_input.get_attribute("value")
            )

            print(
                f"Year after DOWN arrow: {current_year}"
            )

        assert current_year == 2024, (
            f"Year navigation failed. "
            f"Expected 2024, Actual {current_year}"
        )

        print(
            "Year successfully changed: "
            "2026 -> 2025 -> 2024"
        )

        # ---------------------------------------------------------
        # Select January directly from month dropdown
        #
        # Do NOT click month arrows.
        # ---------------------------------------------------------

        month_dropdown = wait.until(
            EC.visibility_of_element_located(
                month_dropdown_locator
            )
        )

        Select(month_dropdown).select_by_visible_text(
            "January"
        )

        wait.until(
            lambda d:
            d.find_element(
                *month_dropdown_locator
            ).get_attribute("value") == "0"
        )

        print(
            "Calendar is now showing January 2024"
        )

        # ---------------------------------------------------------
        # Select 01 Jan 2024
        # ---------------------------------------------------------

        jan_1_locator = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
            "//span[contains(@class,'flatpickr-day') "
            "and @aria-label='January 1, 2024' "
            "and not(contains(@class,'prevMonthDay')) "
            "and not(contains(@class,'nextMonthDay'))]"
        )

        jan_1 = wait.until(
            EC.element_to_be_clickable(
                jan_1_locator
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_1
        )

        print(
            "Selected: 01 Jan 2024"
        )

        # ---------------------------------------------------------
        # Select 02 Jan 2024
        # ---------------------------------------------------------

        jan_2_locator = (
            By.XPATH,
            "//div[contains(@class,'flatpickr-calendar') "
            "and contains(@class,'open')]"
            "//span[contains(@class,'flatpickr-day') "
            "and @aria-label='January 2, 2024' "
            "and not(contains(@class,'prevMonthDay')) "
            "and not(contains(@class,'nextMonthDay'))]"
        )

        jan_2 = wait.until(
            EC.element_to_be_clickable(
                jan_2_locator
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_2
        )

        print(
            "Selected: 02 Jan 2024"
        )

        # =========================================================
        # IMPORTANT FIX
        #
        # DO NOT LOOK FOR / CLICK THE "Filter" BUTTON HERE.
        #
        # In Application Users, selecting the second date causes
        # the date-range filter to be applied automatically.
        #
        # The previous failure happened exactly because the test
        # waited for a Filter button which is not part of this
        # date-filter flow.
        # =========================================================

        # ---------------------------------------------------------
        # Wait until date picker closes
        # ---------------------------------------------------------

        try:
            wait.until(
                lambda d:
                not any(
                    element.is_displayed()
                    for element in d.find_elements(
                        *calendar
                    )
                )
            )
        except Exception:
            # The picker may remain briefly while the table/API
            # request is being processed. This is not a failure.
            pass

        # ---------------------------------------------------------
        # Wait for the application's date filter request/result.
        #
        # The Application Users page updates the URL with:
        # date_range=2024-01-01+to+2024-01-02
        # ---------------------------------------------------------

        wait.until(
            lambda d:
            "date_range=2024-01-01" in d.current_url
            and
            "2024-01-02" in d.current_url
        )

        print(
            f"Date filter applied automatically: "
            f"{page.driver.current_url}"
        )

        # ---------------------------------------------------------
        # Wait for No Result Found
        # ---------------------------------------------------------

        wait.until(
            lambda d: page.has_no_data()
        )

        assert page.has_no_data(), (
            "No Result Found message was not displayed "
            "for invalid date range: "
            "01 Jan 2024 - 02 Jan 2024"
        )

        print(
            "PASS: 01 Jan 2024 - 02 Jan 2024 "
            "-> No Result Found"
        )
