import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.QRcodemonitoring.sa_qr_monitoring_page import (
    SAQRMonitoringPage
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestQRMonitoringExportNegative:

    # =========================================================
    # COMMON
    # =========================================================

    def _open_export(self, page):
        page.goto_page()

        # Same flow as the positive export test cases:
        # open the Export popup first.
        page.click_export()

        WebDriverWait(
            page.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                page.EXPORT_POPUP
            )
        )

    def _submit_empty_export(self, page):
        # Use the existing page-object EXPORT_SUBMIT locator.
        # Do NOT use a generic Submit button from the whole page.
        submit = WebDriverWait(
            page.driver,
            15
        ).until(
            EC.element_to_be_clickable(
                page.EXPORT_SUBMIT
            )
        )

        page.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            submit
        )

        page.driver.execute_script(
            "arguments[0].click();",
            submit
        )

        print("Export Submit clicked without filling details")

    def _get_visible_validation_messages(self, page):
        # Read only validation messages inside Export modal.
        elements = page.driver.find_elements(
            By.XPATH,
            "//div[@id='modeSelectionModal']"
            "//span[contains(@class,'invalid-feedback')"
            " and contains(@class,'d-block')]"
        )

        return [
            element.text.strip()
            for element in elements
            if element.is_displayed() and element.text.strip()
        ]

    def _wait_for_validation(self, page):
        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: len(
                self._get_visible_validation_messages(page)
            ) > 0
        )

        messages = self._get_visible_validation_messages(page)

        for message in messages:
            print(f"Validation: {message}")

        return messages

    # =========================================================
    # 1. ID BASED
    #
    # Positive flow:
    #   goto_page()
    #   click_export()
    #   ID Based is the default tab
    #   fill Start ID / End ID / User
    #   Submit
    #
    # Negative flow:
    #   goto_page()
    #   click_export()
    #   keep everything empty
    #   Submit
    # =========================================================

    def test_export_id_based_empty_submit(self, setup):

        page = SAQRMonitoringPage(setup)

        self._open_export(page)

        # ID Based is the default active tab.
        # Do NOT fill fromId, toId or user.

        print("ID Based tab - submitting empty form")

        self._submit_empty_export(page)

        messages = self._wait_for_validation(page)

        assert "Report Start ID is required." in messages, (
            "ID Based validation for Report Start ID was not displayed. "
            f"Actual messages: {messages}"
        )

        assert "Please select at least one user." in messages, (
            "ID Based validation for User was not displayed. "
            f"Actual messages: {messages}"
        )

        # Based on the actual application validation observed:
        # Report End ID is not displayed until the preceding validation
        # state is satisfied, so do not incorrectly force that message.

        print(
            "PASS: ID Based -> Submit without details -> "
            "required-field validation displayed"
        )

    # =========================================================
    # 2. USER BASED
    #
    # IMPORTANT:
    # Use the SAME page-object tab locator as the positive test:
    #       self.USER_BASED_TAB
    #
    # The previous code failed because it searched for:
    #       <a> or <button> containing "User Based"
    #
    # This application uses the tab ID:
    #       user-tab
    # =========================================================

    def test_export_user_based_empty_submit(self, setup):

        page = SAQRMonitoringPage(setup)

        self._open_export(page)

        print("Opening User Based tab")

        # EXACTLY the locator used by positive flow.
        page.click(page.USER_BASED_TAB)

        WebDriverWait(
            page.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "userTabPane")
            )
        )

        print("User Based tab opened")

        # Do not select user.
        # Do not select date range.
        # Do not select start/end time.

        self._submit_empty_export(page)

        messages = self._wait_for_validation(page)

        assert "Please select at least one user." in messages, (
            "User Based user validation was not displayed. "
            f"Actual messages: {messages}"
        )

        assert "Date range is required." in messages, (
            "User Based date-range validation was not displayed. "
            f"Actual messages: {messages}"
        )

        # The application validates User and Date Range first.
        # When both are empty, time validation is not displayed yet.
        # This is the actual application behavior observed in the test run.

        print(
            "PASS: User Based -> Submit without details -> "
            "User and Date Range validation displayed"
        )

    # =========================================================
    # 3. BULK ID BASED
    #
    # Positive flow uses:
    #       (By.ID, "bulk-tab")
    #
    # Negative flow:
    #       open Export
    #       click Bulk ID Based tab
    #       leave textarea empty
    #       click Submit
    # =========================================================

    def test_export_bulk_id_based_empty_submit(self, setup):

        page = SAQRMonitoringPage(setup)

        self._open_export(page)

        print("Opening Bulk ID Based tab")

        # EXACT locator from the working positive implementation.
        page.click(
            (By.ID, "bulk-tab")
        )

        WebDriverWait(
            page.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "bulkTabPane")
            )
        )

        print("Bulk ID Based tab opened")

        # Do not enter any Bulk IDs.
        self._submit_empty_export(page)

        messages = self._wait_for_validation(page)

        assert "Bulk IDs are required." in messages, (
            "Bulk ID Based validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: Bulk ID Based -> Submit without details -> "
            "required-field validation displayed"
        )

    # =========================================================
    # 4. DATE BASED
    #
    # Positive flow uses:
    #       self.DATE_BASED_TAB
    #       self.DATE_BASED_RANGE
    #
    # Negative flow:
    #       open Export
    #       click Date Based tab
    #       leave date range empty
    #       click Submit
    # =========================================================

    def test_export_date_based_empty_submit(self, setup):

        page = SAQRMonitoringPage(setup)

        self._open_export(page)

        print("Opening Date Based tab")

        # EXACT locator used by positive flow.
        page.click(
            page.DATE_BASED_TAB
        )

        WebDriverWait(
            page.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "dateTabPane")
            )
        )

        print("Date Based tab opened")

        # Do not select any date.
        self._submit_empty_export(page)

        messages = self._wait_for_validation(page)

        assert "Date range is required." in messages, (
            "Date Based date-range validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: Date Based -> Submit without details -> "
            "required-field validation displayed"
        )
