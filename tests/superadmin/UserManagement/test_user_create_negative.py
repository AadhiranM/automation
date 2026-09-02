import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.UserManagement.sa_user_create_page import (
    SAUserCreatePage
)
from pages.superadmin.UserManagement.sa_roles_permissions_page import (
    SARolesPermissionsPage
)

from utilities.data_generator import (
    generate_user_email,
    generate_mobile_number
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestCreateUserNegative:

    # =========================================================
    # COMMON HELPERS
    # =========================================================

    def _visible_text_present(self, page, text):
        return any(
            element.is_displayed()
            for element in page.driver.find_elements(
                By.XPATH,
                f"//*[contains(normalize-space(),'{text}')]"
            )
        )

    def _wait_for_text(self, page, text):
        WebDriverWait(page.driver, 10).until(
            lambda d: self._visible_text_present(page, text)
        )

    def _get_validation_messages(self, page):
        elements = page.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'invalid-feedback') and normalize-space()]"
        )

        return [
            element.text.strip()
            for element in elements
            if element.is_displayed() and element.text.strip()
        ]

    def _click_submit(self, page):
        submit = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.presence_of_element_located(page.SUBMIT_BTN)
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

    def _fill_valid_fields_except_password(self, setup, page):
        """
        Fill every mandatory field with valid data except Password.

        This is required for the password negative tests.
        Otherwise the form stops at Email/Role/Status/Mobile
        validation and the password rule is not the validation
        being tested.
        """

        role_page = SARolesPermissionsPage(setup)

        role_page.goto_list_page()

        role_name = role_page.get_first_row_role_name()

        role_page.search_role(role_name)

        manufacturer = role_page.get_first_manufacturer()

        print(f"Role        : {role_name}")
        print(f"Manufacturer: {manufacturer}")

        page.goto_page()

        page.enter_name("test")

        page.enter_email(
            generate_user_email()
        )

        page.select_manufacturer(
            manufacturer
        )

        page.select_role(
            role_name
        )

        page.select_status(
            "Active"
        )

        page.enter_mobile(
            generate_mobile_number()
        )

    # =========================================================
    # 1. REQUIRED FIELD VALIDATION
    #
    # Enter Name only.
    # Click Submit.
    #
    # Expected:
    # Email, Role, Status and Mobile validations.
    #
    # Password has a separate password-rule message on the UI,
    # but it is not returned as invalid-feedback when empty.
    # =========================================================

    def test_create_user_required_field_validation(self, setup):

        page = SAUserCreatePage(setup)

        page.goto_page()

        page.enter_name("test")

        self._click_submit(page)

        WebDriverWait(
            page.driver,
            10
        ).until(
            lambda d: len(
                self._get_validation_messages(page)
            ) >= 4
        )

        messages = self._get_validation_messages(page)

        print("Validation Messages:")
        for message in messages:
            print(f"  - {message}")

        assert "The email field is required." in messages, (
            f"Email validation was not displayed. "
            f"Actual messages: {messages}"
        )

        assert "The role id field is required." in messages, (
            f"Role validation was not displayed. "
            f"Actual messages: {messages}"
        )

        assert "The status field is required." in messages, (
            f"Status validation was not displayed. "
            f"Actual messages: {messages}"
        )

        assert "The mobile field is required." in messages, (
            f"Mobile validation was not displayed. "
            f"Actual messages: {messages}"
        )

        print(
            "PASS: Required-field validations displayed "
            "after entering only Name and clicking Submit"
        )

    # =========================================================
    # 2. MANUFACTURER REQUIRED
    #
    # Enter Name.
    # Select Manufacturer checkbox.
    # Do not select a Manufacturer.
    # Click Submit.
    #
    # Expected:
    # "Please select a Manufacturer."
    #
    # Manufacturer validation is handled separately by the UI,
    # so do not wait only for invalid-feedback elements.
    # =========================================================

    def test_create_user_manufacturer_required(self, setup):

        page = SAUserCreatePage(setup)

        page.goto_page()

        page.enter_name("test")

        checkbox = WebDriverWait(
            page.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                page.MANUFACTURER_CHECKBOX
            )
        )

        page.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        print("Manufacturer checkbox selected")

        self._click_submit(page)

        self._wait_for_text(
            page,
            "Please select a Manufacturer."
        )

        assert self._visible_text_present(
            page,
            "Please select a Manufacturer."
        ), (
            "Manufacturer validation was not displayed."
        )

        print(
            "PASS: Please select a Manufacturer. "
            "validation displayed"
        )

    # =========================================================
    # 3. PASSWORD - NO UPPERCASE
    #
    # Valid:
    # - lowercase
    # - number
    # - special character
    # - length >= 8
    #
    # Invalid:
    # - uppercase missing
    #
    # Password: testing1!
    # =========================================================

    def test_create_user_password_without_uppercase(self, setup):

        page = SAUserCreatePage(setup)

        self._fill_valid_fields_except_password(
            setup,
            page
        )

        page.enter_password(
            "testing1!"
        )

        self._click_submit(page)

        self._wait_for_text(
            page,
            "Password must contain"
        )

        assert self._visible_text_present(
            page,
            "Password must contain"
        ), (
            "Password validation was not displayed "
            "for password without uppercase character."
        )

        print(
            "PASS: Password without uppercase "
            "was rejected"
        )

    # =========================================================
    # 4. PASSWORD - NO LOWERCASE
    #
    # Valid:
    # - uppercase
    # - number
    # - special character
    # - length >= 8
    #
    # Invalid:
    # - lowercase missing
    #
    # Password: TESTING1!
    # =========================================================

    def test_create_user_password_without_lowercase(self, setup):

        page = SAUserCreatePage(setup)

        self._fill_valid_fields_except_password(
            setup,
            page
        )

        page.enter_password(
            "TESTING1!"
        )

        self._click_submit(page)

        self._wait_for_text(
            page,
            "Password must contain"
        )

        assert self._visible_text_present(
            page,
            "Password must contain"
        ), (
            "Password validation was not displayed "
            "for password without lowercase character."
        )

        print(
            "PASS: Password without lowercase "
            "was rejected"
        )

    # =========================================================
    # 5. PASSWORD - NO SPECIAL CHARACTER
    #
    # Valid:
    # - uppercase
    # - lowercase
    # - number
    # - length >= 8
    #
    # Invalid:
    # - special character missing
    #
    # Password: Testing123
    # =========================================================

    def test_create_user_password_without_special_character(
            self,
            setup
    ):

        page = SAUserCreatePage(setup)

        self._fill_valid_fields_except_password(
            setup,
            page
        )

        page.enter_password(
            "Testing123"
        )

        self._click_submit(page)

        self._wait_for_text(
            page,
            "Password must contain"
        )

        assert self._visible_text_present(
            page,
            "Password must contain"
        ), (
            "Password validation was not displayed "
            "for password without special character."
        )

        print(
            "PASS: Password without special character "
            "was rejected"
        )

    # =========================================================
    # 6. MOBILE - 9 DIGITS
    #
    # Starts with 6.
    # Only 9 digits.
    #
    # Expected:
    # "The mobile field format is invalid."
    # =========================================================

    def test_create_user_mobile_9_digits(self, setup):

        page = SAUserCreatePage(setup)

        page.goto_page()

        page.enter_name("test")

        page.enter_mobile(
            "666666666"
        )

        self._click_submit(page)

        self._wait_for_text(
            page,
            "The mobile field format is invalid."
        )

        assert self._visible_text_present(
            page,
            "The mobile field format is invalid."
        ), (
            "Mobile format validation was not displayed "
            "for 9-digit mobile number."
        )

        print(
            "PASS: 9-digit mobile number "
            "was rejected"
        )

    # =========================================================
    # 7. MOBILE - INVALID STARTING DIGIT
    #
    # Exactly 10 digits but starts with 5.
    #
    # Expected:
    # "The mobile field format is invalid."
    # =========================================================

    def test_create_user_mobile_invalid_start_digit(
            self,
            setup
    ):

        page = SAUserCreatePage(setup)

        page.goto_page()

        page.enter_name("test")

        page.enter_mobile(
            "5666666666"
        )

        self._click_submit(page)

        self._wait_for_text(
            page,
            "The mobile field format is invalid."
        )

        assert self._visible_text_present(
            page,
            "The mobile field format is invalid."
        ), (
            "Mobile format validation was not displayed "
            "for mobile number starting with 5."
        )

        print(
            "PASS: Mobile number starting with 5 "
            "was rejected"
        )
