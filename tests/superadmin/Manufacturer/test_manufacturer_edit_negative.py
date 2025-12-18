import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_edit_page import SAManufacturerEditPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerEditNegative:

    def test_edit_with_empty_email(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        list_page.open_action_menu()
        list_page.click_edit()

        edit_page = SAManufacturerEditPage(setup)
        edit_page.wait_for_page()

        edit_page.update_email("")
        edit_page.update_company_name("Valid Name")
        edit_page.click_update()

        assert edit_page.get_email_value() == ""

    def test_edit_with_empty_company_name(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        list_page.open_action_menu()
        list_page.click_edit()

        edit_page = SAManufacturerEditPage(setup)
        edit_page.wait_for_page()

        edit_page.update_email("valid@mailinator.com")
        edit_page.update_company_name("")
        edit_page.click_update()

        assert edit_page.get_company_name_value() == ""
