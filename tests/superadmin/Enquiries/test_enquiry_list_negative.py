import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryListNegative:

    # =========================================================
    # INVALID SEARCH
    # =========================================================

    def test_search_invalid_enquiry(self, setup):
        page = SAEnquiryListPage(setup)

        page.goto_page()

        wait = WebDriverWait(
            page.driver,
            30
        )

        print("=" * 60)
        print("NEGATIVE ENQUIRY SEARCH TEST")
        print("=" * 60)

        # ---------------------------------------------------------
        # Search field
        # ---------------------------------------------------------

        search_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,"
                    "'Search: ID, Name, Business Email')]"
                )
            )
        )

        search_input.click()
        search_input.clear()

        # ---------------------------------------------------------
        # Invalid ID
        # ---------------------------------------------------------

        invalid_id = "999999999999"

        search_input.send_keys(invalid_id)

        print(
            f"Invalid search value entered: {invalid_id}"
        )

        # ---------------------------------------------------------
        # Make sure value is actually present
        # ---------------------------------------------------------

        wait.until(
            lambda d:
            d.find_element(
                By.XPATH,
                "//input[contains(@placeholder,"
                "'Search: ID, Name, Business Email')]"
            ).get_attribute("value") == invalid_id
        )

        print(
            f"Search value verified: {invalid_id}"
        )

        # ---------------------------------------------------------
        # Click search button
        # ---------------------------------------------------------

        search_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,"
                    "'Search: ID, Name, Business Email')]"
                    "/following-sibling::button"
                )
            )
        )

        search_button.click()

        print("Search button clicked")

        # ---------------------------------------------------------
        # Wait for No Result Found
        # ---------------------------------------------------------

        no_result = (
            By.XPATH,
            "//*[contains(normalize-space(),"
            "'Sorry! No Result Found')]"
        )

        wait.until(
            EC.visibility_of_element_located(
                no_result
            )
        )

        assert page.driver.find_element(
            *no_result
        ).is_displayed(), (
            "No Result Found message was not displayed "
            f"for invalid search: {invalid_id}"
        )

        print(
            f"PASS: Invalid search {invalid_id} "
            "-> No Result Found"
        )

    # =========================================================
    # INVALID CREATED DATE RANGE
    # =========================================================

    def test_filter_invalid_created_date_range(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        wait = WebDriverWait(
            page.driver,
            20,
            poll_frequency=0.5,
            ignored_exceptions=(StaleElementReferenceException,)
        )

        print("=" * 60)
        print("NEGATIVE ENQUIRY DATE FILTER TEST")
        print("=" * 60)

        # Open Created At date picker
        date_filter = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,"
                    "'Filter by : Created At')]"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            date_filter
        )

        print("Date picker opened")

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

        # Current year
        year_input = wait.until(
            EC.visibility_of_element_located(year_input_locator)
        )

        current_year = int(
            year_input.get_attribute("value")
        )

        print(f"Current calendar year: {current_year}")

        # 2026 -> 2025 -> 2024
        while current_year > 2024:

            year_down = wait.until(
                EC.element_to_be_clickable(year_down_locator)
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
                EC.visibility_of_element_located(year_input_locator)
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

        print("Year successfully changed to 2024")

        # Select January directly
        month_dropdown = wait.until(
            EC.visibility_of_element_located(
                month_dropdown_locator
            )
        )

        Select(month_dropdown).select_by_visible_text("January")

        wait.until(
            lambda d:
            d.find_element(
                *month_dropdown_locator
            ).get_attribute("value") == "0"
        )

        print("Calendar is now showing January 2024")

        # Select 01 Jan 2024
        jan_1 = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//span[contains(@class,'flatpickr-day') "
                    "and @aria-label='January 1, 2024' "
                    "and not(contains(@class,'prevMonthDay')) "
                    "and not(contains(@class,'nextMonthDay'))]"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_1
        )

        print("Selected: 01 Jan 2024")

        # Select 02 Jan 2024
        jan_2 = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'flatpickr-calendar') "
                    "and contains(@class,'open')]"
                    "//span[contains(@class,'flatpickr-day') "
                    "and @aria-label='January 2, 2024' "
                    "and not(contains(@class,'prevMonthDay')) "
                    "and not(contains(@class,'nextMonthDay'))]"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            jan_2
        )

        print("Selected: 02 Jan 2024")

        # Wait for the date range to be applied.
        # Enquiries page has a separate Filter button.
        filter_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Filter' "
                    "or .//span[normalize-space()='Filter']]"
                )
            )
        )

        page.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            filter_button
        )

        page.driver.execute_script(
            "arguments[0].click();",
            filter_button
        )

        print("Filter button clicked")

        wait.until(
            lambda d:
            "2024-01-01" in d.current_url
            and "2024-01-02" in d.current_url
        )

        print(
            "Date filter applied: "
            "01 Jan 2024 - 02 Jan 2024"
        )

        wait.until(lambda d: page.has_no_data())

        assert page.has_no_data(), (
            "No Result Found was not displayed "
            "for invalid created date range: "
            "01 Jan 2024 - 02 Jan 2024"
        )

        print(
            "PASS: 01 Jan 2024 - 02 Jan 2024 "
            "-> No Result Found"
        )
