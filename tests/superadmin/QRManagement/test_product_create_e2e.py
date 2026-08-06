import pytest

from pages.superadmin.QRManagement.sa_product_create_parent_page import (
    SAProductCreateParentPage
)
from pages.superadmin.QRManagement.sa_product_create_child_page import (
    SAProductCreateChildPage
)
from pages.superadmin.QRManagement.sa_product_create_video_page import (
    SAProductCreateVideoPage
)
from pages.superadmin.QRManagement.sa_product_list_page import (
    SAProductListPage
)
from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)
from flows.qr_management_flow import QRManagementFlow

@pytest.mark.superadmin
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestProductCreate:

    def get_test_data(self, driver):

        category_page = SACategoryListPage(driver)

        category_page.goto_page()

        manufacturer_name, category_name = (
            category_page.get_first_active_category_and_manufacturer()
        )

        print(
            f"Manufacturer={manufacturer_name}"
            f" | Category={category_name}"
        )

        return manufacturer_name, category_name

    def test_create_product(
            self,
            login_superadmin
    ):
        driver = login_superadmin["driver"]



        flow = QRManagementFlow(driver)

        manufacturer_email, manufacturer_name, category_name = (
            flow.create_category_with_variant()
        )

        list_page = SAProductListPage(driver)

        list_page.goto_page()
        list_page.wait_for_page()
        list_page.click_create()

        parent = SAProductCreateParentPage(driver)

        parent.wait_for_page()

        parent.fill_parent_form(
            manufacturer_email,
            category_name
        )

        child = SAProductCreateChildPage(driver)

        child.open_child_tab()
        child.select_all_variants()
        child.go_to_video()

        video = SAProductCreateVideoPage(driver)

        video.wait_for_page()
        video.create_product()

        list_page.goto_page()

        list_page.wait_for_page()

        list_page.search(
            manufacturer_name
        )

        assert list_page.is_product_present(
            manufacturer_name
        )

