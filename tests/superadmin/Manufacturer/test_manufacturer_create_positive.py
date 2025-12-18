import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_create_page import SAManufacturerCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerCreatePositive:

    def test_create_manufacturer_success(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        list_page.click_add_manufacturer()  # you already have similar buttons
        create = SAManufacturerCreatePage(setup)

        create.fill_email("munich@mailinator.com")
        create.fill_company_name("Munich")
        create.submit()

        create.wait_for_success()
