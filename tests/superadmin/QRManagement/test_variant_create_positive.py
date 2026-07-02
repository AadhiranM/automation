import pytest

from pages.superadmin.QRManagement.sa_variant_list_page import (
    SAVariantListPage
)

from pages.superadmin.QRManagement.sa_variant_create_page import (
    SAVariantCreatePage
)

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)

from utilities.data_generator import (
    generate_variant_type,
    generate_variant_value
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantCreatePositive:

    # ======================================================
    # COMMON TEST DATA
    # ======================================================

    def get_test_data(self, driver):

        category_page = SACategoryListPage(driver)

        category_page.goto_page()

        manufacturer_name, category_name = (
            category_page.get_first_active_category_and_manufacturer()
        )

        print(
            f"Manufacturer={manufacturer_name} | "
            f"Category={category_name}"
        )

        return manufacturer_name, category_name

    # ======================================================
    # OPEN CREATE PAGE + SELECT DATA
    # ======================================================

    def open_create_page(self, driver):

        manufacturer_name, category_name = (
            self.get_test_data(driver)
        )

        list_page = SAVariantListPage(driver)

        list_page.goto_page()

        list_page.click_create()

        create_page = SAVariantCreatePage(driver)

        create_page.wait_for_page()

        create_page.select_manufacturer(
            manufacturer_name
        )

        create_page.select_category(
            category_name
        )

        return (
            list_page,
            create_page,
            manufacturer_name,
            category_name
        )

    # ======================================================
    # SINGLE VARIANT
    # ======================================================

    def test_create_variant_single(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]
        username = login_superadmin["username"]
        print("Username from fixture:", username)

        (
            list_page,
            create_page,
            manufacturer_name,
            category_name
        ) = self.open_create_page(driver)

        create_page.enter_variant_type(
            generate_variant_type()
        )

        create_page.enter_variant_value(
            generate_variant_value()
        )

        create_page.click_save()

        create_page.wait_until_redirected_to_variant_list()

        list_page.search(category_name)

        list_page.wait_for_table_refresh()

        assert list_page.is_category_present(category_name)

        assert list_page.is_created_by_present(username)

    # ======================================================
    # MULTIPLE VARIANT SECTIONS
    # ======================================================

    def test_create_multiple_variant_sections(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]

        (
            list_page,
            create_page,
            manufacturer_name,
            category_name
        ) = self.open_create_page(driver)

        create_page.enter_variant_type(
            generate_variant_type(),
            index=0
        )

        create_page.enter_variant_value(
            generate_variant_value(),
            index=0
        )

        create_page.click_add_more_variants()

        create_page.enter_variant_type(
            generate_variant_type(),
            index=1
        )

        create_page.enter_variant_value(
            generate_variant_value(),
            index=1
        )

        create_page.click_save()

        create_page.wait_until_redirected_to_variant_list()

        list_page.search(category_name)

        list_page.wait_for_table_refresh()

        assert list_page.is_category_present(category_name)


    # ======================================================
    # MULTIPLE VALUES
    # ======================================================

    def test_create_multiple_variant_values(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]

        (
            list_page,
            create_page,
            manufacturer_name,
            category_name
        ) = self.open_create_page(driver)

        create_page.enter_variant_type(
            generate_variant_type(),
            index=0
        )

        create_page.enter_variant_value(
            generate_variant_value(),
            index=0
        )

        create_page.click_add_variant_value()

        create_page.enter_variant_value(
            generate_variant_value(),
            index=1
        )

        create_page.click_add_variant_value()

        create_page.enter_variant_value(
            generate_variant_value(),
            index=2
        )

        create_page.click_save()

        create_page.wait_until_redirected_to_variant_list()

        list_page.search(category_name)

        list_page.wait_for_table_refresh()

        assert list_page.is_category_present(category_name)



    # ======================================================
    # MULTIPLE SECTIONS + MULTIPLE VALUES
    # ======================================================

    def test_create_variant_multiple_sections_and_values(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]

        (
            list_page,
            create_page,
            manufacturer_name,
            category_name
        ) = self.open_create_page(driver)

        create_page.enter_variant_type(
            generate_variant_type(),
            index=0
        )

        create_page.enter_variant_value(
            generate_variant_value(),
            index=0
        )

        create_page.click_add_variant_value()

        create_page.enter_variant_value(
            generate_variant_value(),
            index=1
        )

        create_page.click_add_more_variants()

        create_page.enter_variant_type(
            generate_variant_type(),
            index=1
        )

        create_page.enter_variant_value(
            generate_variant_value(),
            index=2
        )

        create_page.click_save()

        create_page.wait_until_redirected_to_variant_list()

        list_page.search(category_name)

        list_page.wait_for_table_refresh()

        assert list_page.is_category_present(category_name)