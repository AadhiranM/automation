import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.UserManagement.sa_roles_permissions_page import (
    SARolesPermissionsPage
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestRolesPermissionsNegative:

    # =========================================================
    # COMMON HELPERS
    # =========================================================

    def _get_validation_messages(self, page):
        """
        Get all visible validation messages that use the
        standard invalid-feedback class.
        """

        elements = page.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'invalid-feedback') "
            "and normalize-space()]"
        )

        return [
            element.text.strip()
            for element in elements
            if element.is_displayed() and element.text.strip()
        ]

    def _wait_for_validation_count(self, page, minimum_count):
        """
        Wait until the expected number of standard validation
        messages are displayed.
        """

        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: len(
                self._get_validation_messages(page)
            ) >= minimum_count
        )

    def _wait_for_text(self, page, text):
        """
        Wait until the exact validation text is displayed.

        Manufacturer validation is handled separately because
        it is not exposed through the standard invalid-feedback
        locator.
        """

        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: any(
                element.is_displayed()
                and text in element.text.strip()
                for element in d.find_elements(
                    By.XPATH,
                    "//*[normalize-space()]"
                )
            )
        )

    def _click_submit(self, page):
        """
        Click Submit after Angular has enabled it.
        """

        submit = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.presence_of_element_located(
                page.SUBMIT_BTN
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

        print("Submit clicked")

    # =========================================================
    # REQUIRED FIELD + MANUFACTURER VALIDATION
    #
    # STEP 1
    # ---------------------------------------------------------
    # Submit is initially disabled.
    #
    # Enter Role Name.
    # Submit becomes enabled.
    #
    # Click Submit without selecting:
    # - User Type
    # - Status
    # - Permissions
    # - Manufacturer
    #
    # Expected:
    # - User Type required
    # - Status required
    # - Permissions required
    #
    # Manufacturer validation should NOT appear because
    # Manufacturer checkbox is not selected.
    #
    # STEP 2
    # ---------------------------------------------------------
    # Select Manufacturer checkbox.
    # Do NOT select a manufacturer.
    # Click Submit.
    #
    # Expected:
    # - Please select a Manufacturer.
    #
    # User Type / Status / Permissions validations may
    # continue to remain displayed.
    # =========================================================

    @pytest.mark.sanity
    def test_create_role_required_and_manufacturer_validation(
            self,
            setup
    ):

        page = SARolesPermissionsPage(setup)

        page.goto_page()

        print("=" * 60)
        print("NEGATIVE ADD ROLES & PERMISSIONS TEST")
        print("=" * 60)

        # -----------------------------------------------------
        # STEP 1 - VERIFY SUBMIT IS INITIALLY DISABLED
        # -----------------------------------------------------

        submit = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.presence_of_element_located(
                page.SUBMIT_BTN
            )
        )

        assert not submit.is_enabled(), (
            "Submit button should be disabled initially "
            "when Role Name is empty."
        )

        print("PASS: Submit button is disabled initially")

        # -----------------------------------------------------
        # STEP 2 - ENTER ROLE NAME
        # -----------------------------------------------------

        page.enter_role_name("Test Negative Role")

        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: d.find_element(
                *page.SUBMIT_BTN
            ).is_enabled()
        )

        print(
            "Role Name entered: Test Negative Role"
        )

        print(
            "PASS: Submit button became enabled "
            "after entering Role Name"
        )

        # -----------------------------------------------------
        # STEP 3 - SUBMIT WITHOUT OTHER DETAILS
        #
        # Manufacturer checkbox remains unchecked.
        # -----------------------------------------------------

        self._click_submit(page)

        self._wait_for_validation_count(
            page,
            3
        )

        messages = self._get_validation_messages(page)

        print("Validation Messages:")

        for message in messages:
            print(f"  - {message}")

        # -----------------------------------------------------
        # VERIFY USER TYPE VALIDATION
        # -----------------------------------------------------

        assert "The user type field is required." in messages, (
            "User Type validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: User Type required validation displayed"
        )

        # -----------------------------------------------------
        # VERIFY STATUS VALIDATION
        # -----------------------------------------------------

        assert "The status field is required." in messages, (
            "Status validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: Status required validation displayed"
        )

        # -----------------------------------------------------
        # VERIFY PERMISSIONS VALIDATION
        # -----------------------------------------------------

        assert "The permissions field is required." in messages, (
            "Permissions validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: Permissions required validation displayed"
        )

        # -----------------------------------------------------
        # VERIFY MANUFACTURER VALIDATION IS NOT DISPLAYED
        # -----------------------------------------------------

        assert "Please select a Manufacturer." not in messages, (
            "Manufacturer validation should not be displayed "
            "when Manufacturer checkbox is not selected."
        )

        print(
            "PASS: Manufacturer validation not displayed "
            "while checkbox is unchecked"
        )

        # -----------------------------------------------------
        # STEP 4 - SELECT MANUFACTURER CHECKBOX
        # -----------------------------------------------------

        manufacturer_checkbox = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                page.MANUFACTURER_CHECKBOX
            )
        )

        page.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            manufacturer_checkbox
        )

        page.driver.execute_script(
            "arguments[0].click();",
            manufacturer_checkbox
        )

        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: d.find_element(
                *page.MANUFACTURER_CHECKBOX
            ).is_selected()
        )

        print(
            "Manufacturer checkbox selected"
        )

        # -----------------------------------------------------
        # STEP 5 - SUBMIT WITHOUT SELECTING MANUFACTURER
        # -----------------------------------------------------

        self._click_submit(page)

        # IMPORTANT:
        # Do NOT wait for validation count = 4.
        # Manufacturer validation does not use the same
        # invalid-feedback locator.
        self._wait_for_text(
            page,
            "Please select a Manufacturer."
        )

        manufacturer_validation = any(
            element.is_displayed()
            and "Please select a Manufacturer."
            in element.text.strip()
            for element in page.driver.find_elements(
                By.XPATH,
                "//*[normalize-space()]"
            )
        )

        assert manufacturer_validation, (
            "Manufacturer validation was not displayed "
            "after selecting the Manufacturer checkbox "
            "without selecting a Manufacturer."
        )

        print(
            "PASS: Please select a Manufacturer. "
            "validation displayed"
        )

        print("=" * 60)
        print(
            "NEGATIVE TEST PASSED"
        )
        print(
            "Required validations and Manufacturer checkbox "
            "validation were successfully verified."
        )
        print("=" * 60)
