import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_edit_page import SAManufacturerEditPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerEditPositive:

    def test_edit_pending_manufacturer_and_verify_update(self, setup):
        # 🔹 Go to Manufacturer list
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        # 🔹 Open action → Edit
        list_page.open_action_menu()
        list_page.click_edit()

        # 🔹 Edit modal
        edit_page = SAManufacturerEditPage(setup)
        edit_page.wait_for_page()

        # 🔹 Use FIXED, CLEAN values (not derived)
        new_email = "pea_updated@mailinator.com"
        new_company = "Pea Updated"

        # 🔹 Clear + update
        edit_page.update_email(new_email)
        edit_page.update_company_name(new_company)
        edit_page.click_update()

        # 🔹 Wait for modal to close
        edit_page.wait_for_modal_close()

        # 🔹 Re-open SAME row → Edit
        list_page.open_action_menu()
        list_page.click_edit()

        edit_page.wait_for_page()

        # 🔹 Verify updated values
        assert edit_page.get_email_value() == new_email
        assert edit_page.get_company_name_value() == new_company
