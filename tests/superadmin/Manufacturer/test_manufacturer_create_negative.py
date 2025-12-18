import pytest
from selenium.common.exceptions import TimeoutException
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_create_page import SAManufacturerCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerCreateNegative:

    def test_empty_fields(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()
        list_page.click_add_manufacturer()

        create = SAManufacturerCreatePage(setup)
        create.submit()

        assert create.is_email_error_visible()
        assert create.is_company_error_visible()

    def test_invalid_email(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()
        list_page.click_add_manufacturer()

        create = SAManufacturerCreatePage(setup)
        create.fill_email("invalid")
        create.fill_company_name("Test")
        create.submit()

        assert create.is_email_error_visible()
