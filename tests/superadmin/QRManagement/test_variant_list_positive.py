import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage
from pages.superadmin.QRManagement.sa_variant_view_page import SAVariantViewPage
from pages.superadmin.QRManagement.sa_variant_create_page import SAVariantCreatePage
from utilities.data_generator import (
    generate_variant_type,
    generate_variant_value
)

@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantListPositive:

    def test_search_variant(self, setup):
        page = SAVariantListPage(setup)

        page.goto_page()

        page.wait_for_table()

        variant_type = page.get_first_variant_type()

        page.search(
            variant_type
        )

        assert page.is_row_present()

    def test_search_manufacturer(self, setup):
        page = SAVariantListPage(setup)

        page.goto_page()

        page.wait_for_table()

        manufacturer = page.get_first_manufacturer_name()

        page.search(
            manufacturer
        )

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

        # Select first row that contains View option
        list_page.click_actions_with_option(
            require_view=True
        )

        list_page.click_view()

        # Wait for navigation to View page
        WebDriverWait(driver, 10).until(
            lambda d: "viewvariant" in d.current_url.lower()
        )

        view_page = SAVariantViewPage(driver)

        assert view_page.is_view_page_opened()
    def test_edit_variant(self, login_superadmin):
        driver = login_superadmin["driver"]

        list_page = SAVariantListPage(driver)

        list_page.goto_page()
        list_page.wait_for_table()

        list_page.click_actions_with_option(
            require_edit=True
        )

        list_page.click_edit()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(@class,'variant-submit-btn')]"
                )
            )
        )

        edit_page = SAVariantCreatePage(driver)

        variant_type = generate_variant_type()
        variant_value = generate_variant_value()

        edit_page.enter_variant_type(
            variant_type
        )

        edit_page.enter_variant_value(
            variant_value
        )

        edit_page.click_update()

        # Back to list page
        list_page.goto_page()
        list_page.wait_for_table()

        # Open same row in view mode
        list_page.click_actions_with_option(
            require_view=True
        )

        list_page.click_view()

        view_page = SAVariantViewPage(driver)

        assert (
                view_page.get_variant_type().lower()
                == variant_type.lower()
        )

        assert (
                view_page.get_variant_value().lower()
                == variant_value.lower()
        )