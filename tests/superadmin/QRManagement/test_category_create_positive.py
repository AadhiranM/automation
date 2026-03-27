import pytest
from pages.superadmin.QRManagement.sa_category_list_page import SACategoryListPage
from pages.superadmin.QRManagement.sa_category_create_page import SACategoryCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreatePositive:

    def test_create_category_success(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        # Open modal
        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        # Test data
        category_name = "BerlinAutomateTest"

        # Fill form
        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.enter_category_name(category_name)
        create_page.select_status("Active")

        # Save
        create_page.click_save()

        msg = create_page.get_success_message()
        assert "Category Created Successfully" in msg

        # Validate in table
        assert list_page.is_category_present(category_name)