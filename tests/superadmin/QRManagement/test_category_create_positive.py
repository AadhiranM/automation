import pytest
from pages.superadmin.QRManagement.sa_category_list_page import SACategoryListPage
from pages.superadmin.QRManagement.sa_category_create_page import SACategoryCreatePage
from utilities.data_generator import generate_category_name

@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreatePositive:

    def test_create_category_inactive(self, setup,category_name):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.select_manufacturer()
        create_page.enter_category_name(category_name)
        create_page.select_status("Inactive")

        create_page.click_save()

        create_page.wait_for_modal_to_close()
        list_page.wait_for_table_refresh()

        # ✅ Validate row exists
        assert list_page.is_category_present(category_name)

        # ✅ Validate status
        status = list_page.get_category_status(category_name)
        assert status == "Inactive"

    def test_create_category_active(self, setup,category_name):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()


        create_page.select_manufacturer()
        create_page.enter_category_name(category_name)
        create_page.select_status("Active")

        create_page.click_save()

        create_page.wait_for_modal_to_close()
        list_page.wait_for_table_refresh()

        assert list_page.is_category_present(category_name)

        status = list_page.get_category_status(category_name)
        assert status == "Active"

