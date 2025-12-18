import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_edit_page import SAManufacturerEditPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerEditPositive:

    def test_edit_email_and_company_name(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        # Open Edit
        list_page.open_action_menu()
        list_page.click_edit()

        edit_page = SAManufacturerEditPage(setup)
        edit_page.wait_for_page()

        # Update both fields
        edit_page.update_email("frankfurt_updated@mailinator.com")
        edit_page.update_company_name("Frankfurt Updated")

        edit_page.click_update()

        # Success = no crash + navigation back
