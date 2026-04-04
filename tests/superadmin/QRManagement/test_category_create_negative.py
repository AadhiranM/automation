import pytest
from pages.superadmin.QRManagement.sa_category_list_page import SACategoryListPage
from pages.superadmin.QRManagement.sa_category_create_page import SACategoryCreatePage
from utilities.data_generator import generate_category_name

@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreateNegative:

    def test_blank_manufacture_name(self, setup,category_name):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()
        create_page.enter_category_name(category_name)
        create_page.click_save()

        assert create_page.is_error_present("Please select a manufacturer.")


    def test_blank_category_name(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.select_manufacturer("Sydneyyy Tea Shop")

        # ✅ ADDED LINE (IMPORTANT)
        assert create_page.is_manufacturer_selected("Sydneyyy Tea Shop")

        create_page.click_save()

        assert create_page.is_error_present("The category is required.")


    def test_all_fields_blank(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.click_save()

        assert create_page.is_error_present("Please select a manufacturer.")
        assert create_page.is_error_present("The category is required.")


    def test_invalid_category_name(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.select_manufacturer("Sydneyyy Tea Shop")

        # ✅ ADDED LINE (IMPORTANT)
        assert create_page.is_manufacturer_selected("Sydneyyy Tea Shop")

        create_page.enter_category_name("123456")

        create_page.click_save()

        assert create_page.is_error_present("The category should contain only letters and spaces.")