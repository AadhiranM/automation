import pytest
from pages.superadmin.QRManagement.sa_product_create_parent_page import SAProductCreateParentPage
from pages.superadmin.QRManagement.sa_product_create_child_page import SAProductCreateChildPage
from pages.superadmin.QRManagement.sa_product_create_video_page import SAProductCreateVideoPage
from pages.superadmin.QRManagement.sa_product_list_page import SAProductListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestProductCreate:

    def test_create_product(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAProductListPage(driver)

        # ✅ Step 1: Navigate
        list_page.goto_page()
        list_page.wait_for_page()

        # ✅ Step 2: Click Create
        list_page.click_create()

        # ✅ Step 3: Parent Page
        parent = SAProductCreateParentPage(driver)
        parent.wait_for_page()
        parent.fill_parent_form()
        parent.go_to_child()

        # ✅ Step 4: Child Page
        child = SAProductCreateChildPage(driver)
        child.open_child_tab()
        child.select_variant()
        child.go_to_video()

        # ✅ Step 5: Video Page
        video = SAProductCreateVideoPage(driver)
        video.wait_for_page()
        video.create_product()

        # ✅ FINAL ASSERTION
        assert video.is_product_created_successfully()