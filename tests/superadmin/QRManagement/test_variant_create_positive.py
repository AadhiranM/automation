import pytest
from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage
from pages.superadmin.QRManagement.sa_variant_create_page import SAVariantCreatePage
from utilities.data_generator import generate_variant_type, generate_variant_value

@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantCreatePositive:

    def test_create_variant_single(self, login_superadmin):
        driver = login_superadmin["driver"]
        username = login_superadmin["username"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(driver)
        create_page.wait_for_page()

        category_name = "BerlinAutomateTest"

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category(category_name)

        variant_type = generate_variant_type()
        variant_value = generate_variant_value()

        create_page.enter_variant_type(variant_type)
        create_page.enter_variant_value(variant_value)

        create_page.click_save()

        assert create_page.is_variant_saved_successfully()

        # Reload list page (IMPORTANT)
        list_page.goto_page()
        list_page.search(category_name)
        list_page.wait_for_table_refresh()

        # ✅ VALIDATIONS

        assert list_page.is_category_present(category_name)
        assert list_page.is_created_by_present(username)

    def test_create_multiple_variant_sections(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(driver)
        create_page.wait_for_page()

        category_name = "BerlinAutomateTest"

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category(category_name)

        # First section
        create_page.enter_variant_type(generate_variant_type(), index=0)
        create_page.enter_variant_value(generate_variant_value(), index=0)

        # Add second section
        create_page.click_add_more_variants()

        create_page.enter_variant_type(generate_variant_type(), index=1)
        create_page.enter_variant_value(generate_variant_value(), index=1)

        create_page.click_save()

        assert create_page.is_variant_saved_successfully()

    def test_create_multiple_variant_values(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(driver)
        create_page.wait_for_page()

        category_name = "BerlinAutomateTest"

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category(category_name)

        create_page.enter_variant_type(generate_variant_type(), index=0)

        # First value
        create_page.enter_variant_value(generate_variant_value(), index=0)

        # Add multiple values
        create_page.click_add_variant_value()
        create_page.enter_variant_value(generate_variant_value(), index=1)

        create_page.click_add_variant_value()
        create_page.enter_variant_value(generate_variant_value(), index=2)

        create_page.click_save()

        assert create_page.is_variant_saved_successfully()

    def test_create_variant_multiple_sections_and_values(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(driver)
        create_page.wait_for_page()

        category_name = "BerlinAutomateTest"

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category(category_name)

        # Section 1
        create_page.enter_variant_type(generate_variant_type(), index=0)
        create_page.enter_variant_value(generate_variant_value(), index=0)

        create_page.click_add_variant_value()
        create_page.enter_variant_value(generate_variant_value(), index=1)

        # Section 2
        create_page.click_add_more_variants()

        create_page.enter_variant_type(generate_variant_type(), index=1)
        create_page.enter_variant_value(generate_variant_value(), index=2)

        create_page.click_save()

        assert create_page.is_variant_saved_successfully()