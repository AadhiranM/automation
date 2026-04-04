import pytest
from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage
from pages.superadmin.QRManagement.sa_variant_create_page import SAVariantCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantCreateNegative:

    def test_blank_manufacturer(self, setup):
        list_page = SAVariantListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(setup)
        create_page.wait_for_page()

        create_page.click_save()

        assert create_page.is_error_present("manufacturer")

    def test_blank_category(self, setup):
        list_page = SAVariantListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(setup)
        create_page.wait_for_page()

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")

        create_page.click_save()

        assert create_page.is_error_present("category")

    def test_blank_variant_type(self, setup):
        list_page = SAVariantListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(setup)
        create_page.wait_for_page()

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category("BerlinAutomateTest")

        create_page.enter_variant_value("Test")

        create_page.click_save()

        assert create_page.is_error_present("variant")

    def test_blank_variant_value(self, setup):
        list_page = SAVariantListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(setup)
        create_page.wait_for_page()

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category("BerlinAutomateTest")

        create_page.enter_variant_type("Size")

        create_page.click_save()

        assert create_page.is_error_present("variant")

    def test_all_fields_blank(self, setup):
        list_page = SAVariantListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(setup)
        create_page.wait_for_page()

        create_page.click_save()

        errors = create_page.get_all_errors()

        assert len(errors) > 0