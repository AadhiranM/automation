import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)

from pages.superadmin.QRManagement.sa_category_create_page import (
    SACategoryCreatePage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreatePositive:

    def test_create_category_inactive(self, setup, category_name):
        manufacturer_page = SAManufacturerListPage(setup)

        manufacturer_page.goto_page()

        manufacturer_email = (
            manufacturer_page.get_first_approved_business_email()
        )

        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.select_manufacturer(manufacturer_email)
        create_page.enter_category_name(category_name)
        create_page.select_status("Active")

        create_page.click_save()

        create_page.wait_for_modal_to_close()

    def test_create_category_active(self, setup, category_name):
        manufacturer_page = SAManufacturerListPage(setup)

        manufacturer_page.goto_page()

        manufacturer_email = (
            manufacturer_page.get_first_approved_business_email()
        )

        list_page = SACategoryListPage(setup)
        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)
        create_page.wait_for_modal()

        create_page.select_manufacturer(manufacturer_email)
        create_page.enter_category_name(category_name)
        create_page.select_status("Active")

        create_page.click_save()

        create_page.wait_for_modal_to_close()