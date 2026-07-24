from utilities.data_generator import (
    generate_category_name,
    generate_variant_type,
    generate_variant_value,
)

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage,
)

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage,
)
from pages.superadmin.QRManagement.sa_category_create_page import (
    SACategoryCreatePage,
)

from pages.superadmin.QRManagement.sa_variant_list_page import (
    SAVariantListPage,
)
from pages.superadmin.QRManagement.sa_variant_create_page import (
    SAVariantCreatePage,
)


class QRManagementFlow:

    def __init__(self, driver):
        self.driver = driver

    # =====================================================
    # CATEGORY
    # =====================================================

    def create_active_category(self):

        manufacturer_page = SAManufacturerListPage(self.driver)
        manufacturer_page.goto_page()

        manufacturer_email, manufacturer_name = (
            manufacturer_page.get_first_approved_manufacturer()
        )

        category_name = generate_category_name()

        list_page = SACategoryListPage(self.driver)
        list_page.goto_page()
        list_page.click_create()

        create_page = SACategoryCreatePage(self.driver)
        create_page.wait_for_modal()

        create_page.select_manufacturer(manufacturer_name)
        create_page.enter_category_name(category_name)
        create_page.select_status("Active")

        create_page.click_save()
        create_page.wait_for_modal_to_close()

        return (
            manufacturer_email,
            manufacturer_name,
            category_name
        )

    # =====================================================
    # VARIANT
    # =====================================================

    def create_single_variant(
        self,
        manufacturer_name,
        category_name
    ):

        list_page = SAVariantListPage(self.driver)

        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(self.driver)
        create_page.wait_for_page()

        create_page.select_manufacturer(
            manufacturer_name
        )

        create_page.select_category(
            category_name
        )

        create_page.enter_variant_type(
            generate_variant_type()
        )

        create_page.enter_variant_value(
            generate_variant_value()
        )

        create_page.click_save()

        create_page.wait_until_redirected_to_variant_list()

    # =====================================================
    # PRODUCT PREPARATION
    # =====================================================

    def create_category_with_variant(self):
        manufacturer_email, manufacturer_name, category_name = (
            self.create_active_category()
        )

        self.create_single_variant(
            manufacturer_name,
            category_name
        )

        return (
            manufacturer_email,
            manufacturer_name,
            category_name
        )