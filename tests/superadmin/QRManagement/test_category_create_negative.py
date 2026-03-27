import pytest
from pages.superadmin.QRManagement.sa_category_list_page import SACategoryListPage
from pages.superadmin.QRManagement.sa_category_create_page import SACategoryCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreateNegative:

    def test_blank_category_name(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        # Only manufacturer selected
        create_page.select_manufacturer("Sydneyy Tea Shop")

        create_page.click_save()

        assert create_page.is_category_error_visible()

    def test_all_fields_blank(self, setup):
        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.click_save()

        assert create_page.is_category_error_visible()