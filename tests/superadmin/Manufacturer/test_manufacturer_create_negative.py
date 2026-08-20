import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.Manufacturer.sa_manufacturer_create_page import (
    SAManufacturerCreatePage
)

from utilities.data_generator import (
    generate_mailinator_email,
    generate_manufacturer_name
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerCreateNegative:

    # ============================================================
    # 1. EXISTING COMPANY + EXISTING EMAIL
    # ============================================================
    @pytest.mark.negative
    @pytest.mark.sanity
    def test_create_manufacturer_duplicate_company_and_email(self, setup):

        list_page = SAManufacturerListPage(setup)
        create_page = SAManufacturerCreatePage(setup)

        # Open Manufacturer List
        list_page.goto_page()

        # Get existing manufacturer details
        existing_company = list_page.get_first_row_company()
        existing_email = list_page.get_first_row_email()

        print(f"Existing Company : {existing_company}")
        print(f"Existing Email   : {existing_email}")

        assert existing_company, \
            "Existing company name was not found"

        assert existing_email, \
            "Existing email was not found"

        # Open Create Manufacturer
        list_page.click_create()

        create_page.wait_for_page()

        # Allow backend validation
        create_page.disable_browser_validation()

        # Enter existing values
        create_page.fill_company_name(existing_company)
        create_page.fill_email(existing_email)

        # Save
        create_page.click_save()

        # Validate Company error
        company_error = WebDriverWait(setup, 10).until(
            EC.visibility_of_element_located(
                create_page.ERROR_COMPANY
            )
        )

        assert company_error.text.strip() == \
            "The Company Name has already been taken."

        # Validate Email error
        email_error = WebDriverWait(setup, 10).until(
            EC.visibility_of_element_located(
                create_page.ERROR_EMAIL
            )
        )

        assert email_error.text.strip() == \
            "The email has already been taken."

        print(
            "Duplicate company + duplicate email "
            "validation passed"
        )

    # ============================================================
    # 2. EXISTING COMPANY + NEW EMAIL
    # ============================================================
    @pytest.mark.negative
    @pytest.mark.sanity
    def test_create_manufacturer_existing_company_new_email(self, setup):

        list_page = SAManufacturerListPage(setup)
        create_page = SAManufacturerCreatePage(setup)

        # Open Manufacturer List
        list_page.goto_page()

        # Get existing company from first row
        existing_company = list_page.get_first_row_company()

        assert existing_company, \
            "Existing company name was not found"

        # Generate NEW email
        new_email = generate_mailinator_email()

        print(f"Existing Company : {existing_company}")
        print(f"New Email        : {new_email}")

        # Open Create Manufacturer
        list_page.click_create()

        create_page.wait_for_page()

        # Allow backend validation
        create_page.disable_browser_validation()

        # Existing company
        create_page.fill_company_name(existing_company)

        # NEW email
        create_page.fill_email(new_email)

        # Save
        create_page.click_save()

        # Company should show duplicate validation
        company_error = WebDriverWait(setup, 10).until(
            EC.visibility_of_element_located(
                create_page.ERROR_COMPANY
            )
        )

        assert company_error.text.strip() == \
            "The Company Name has already been taken.", \
            f"Unexpected company error: {company_error.text}"

        # Email should NOT show duplicate validation
        assert not create_page.is_email_error_visible(), \
            "Email duplicate validation appeared for a new email"

        print(
            "Existing company + new email "
            "validation passed"
        )

    # ============================================================
    # 3. NEW COMPANY + EXISTING EMAIL
    # ============================================================
    @pytest.mark.negative
    @pytest.mark.sanity
    def test_create_manufacturer_new_company_existing_email(self, setup):

        list_page = SAManufacturerListPage(setup)
        create_page = SAManufacturerCreatePage(setup)

        # Open Manufacturer List
        list_page.goto_page()

        # Get existing email from first row
        existing_email = list_page.get_first_row_email()

        assert existing_email, \
            "Existing email was not found"

        # Generate NEW company name
        new_company = generate_manufacturer_name()

        print(f"New Company      : {new_company}")
        print(f"Existing Email   : {existing_email}")

        # Open Create Manufacturer
        list_page.click_create()

        create_page.wait_for_page()

        # Allow backend validation
        create_page.disable_browser_validation()

        # NEW company
        create_page.fill_company_name(new_company)

        # Existing email
        create_page.fill_email(existing_email)

        # Save
        create_page.click_save()

        # Email should show duplicate validation
        email_error = WebDriverWait(setup, 10).until(
            EC.visibility_of_element_located(
                create_page.ERROR_EMAIL
            )
        )

        assert email_error.text.strip() == \
            "The email has already been taken.", \
            f"Unexpected email error: {email_error.text}"

        # Company should NOT show duplicate validation
        assert not create_page.is_company_error_visible(), \
            "Company duplicate validation appeared for a new company"

        print(
            "New company + existing email "
            "validation passed"
        )