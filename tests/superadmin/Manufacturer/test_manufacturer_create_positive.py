import pytest
from selenium.webdriver.support.ui import WebDriverWait

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
class TestManufacturerCreatePositive:

    def test_create_manufacturer_success(self, setup):

        list_page = SAManufacturerListPage(setup)
        create_page = SAManufacturerCreatePage(setup)

        list_page.goto_page()

        # Open Create Modal
        list_page.click_create()

        create_page.wait_for_page()

        # Dynamic CI/CD data
        company_name = generate_manufacturer_name()
        email = generate_mailinator_email()

        print(f"Creating Company : {company_name}")
        print(f"Creating Email   : {email}")

        # Create Manufacturer
        create_page.fill_email(email)
        create_page.fill_company_name(company_name)
        create_page.click_save()

        # Wait until manufacturer appears in grid
        WebDriverWait(setup, 20).until(
            lambda d: list_page.is_company_present(company_name)
        )

        # Final Validation
        assert list_page.is_company_present(company_name), \
            f"Manufacturer not found in grid: {company_name}"

        print(f"Manufacturer created successfully: {company_name}")