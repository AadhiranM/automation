import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_create_page import SAManufacturerCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerCreatePositive:

    def test_create_manufacturer_success(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        # Open Create modal
        list_page.click_create()

        create_page = SAManufacturerCreatePage(setup)
        create_page.wait_for_page()

        # Enter details
        create_page.fill_email("Sydneyy@mailinator.com")
        create_page.fill_company_name("Sydneyy Tea Shop")

        # Save
        create_page.click_save()
        msg = create_page.wait_for_success()
        assert "Created Successfully" in msg

        # secondary validation
        assert list_page.is_company_present("Sydney Tea Shop")
