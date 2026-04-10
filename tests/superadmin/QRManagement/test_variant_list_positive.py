import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage
from pages.superadmin.QRManagement.sa_variant_view_page import SAVariantViewPage
from pages.superadmin.QRManagement.sa_variant_create_page import SAVariantCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantListPositive:

    def test_search_variant(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.wait_for_table()

        page.search("hill")

        assert page.is_row_present()

    def test_search_manufacturer(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.wait_for_table()

        page.search("Sydney Tea Shop Pvt Ltd")

        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.wait_for_table()

        page.set_entries_per_page(25)

        assert page.is_row_present()

    def test_pagination(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.wait_for_table()

        page.click_next()
        page.wait_for_table()
        assert page.is_row_present()

        page.click_previous()
        page.wait_for_table()
        assert page.is_row_present()

    def test_search_and_refresh(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.wait_for_table()

        # Search invalid
        list_page.search("random_not_exist")

        # ✅ STRONG WAIT for "No Data"
        WebDriverWait(driver, 10).until(
            lambda d: list_page.is_no_result_displayed()
        )
        assert list_page.is_no_result_displayed()

        # Refresh
        list_page.click_refresh()
        list_page.wait_for_table()

        # ✅ wait until data comes back
        WebDriverWait(driver, 10).until(
            lambda d: not list_page.is_no_result_displayed()
        )

        assert not list_page.is_no_result_displayed()

    def test_view_variant(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.wait_for_table()

        # ✅ MUST pick row with VIEW
        list_page.click_actions_with_option(require_view=True)
        list_page.click_view()

        # ✅ WAIT FOR VIEW PAGE LOAD (IMPORTANT FIX)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input"))
        )

        view_page = SAVariantViewPage(driver)

        assert view_page.are_fields_disabled()

    def test_edit_variant(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.wait_for_table()

        # ✅ MUST pick row with EDIT
        list_page.click_actions_with_option(require_edit=True)
        list_page.click_edit()

        # ✅ WAIT FOR EDIT PAGE LOAD (FIXED)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@class,'variant-submit-btn')]")
            )
        )

        # ✅ reuse create page (correct)
        edit_page = SAVariantCreatePage(driver)

        edit_page.enter_variant_value("UpdatedValue")
        edit_page.click_update()

        # ✅ wait for toast
        WebDriverWait(driver, 10).until(
            lambda d: "success" in edit_page.get_toast_message().lower()
        )

        assert "success" in edit_page.get_toast_message().lower()