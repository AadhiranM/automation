import pytest
from datetime import date, timedelta
from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantListPositive:

    def test_search_variant(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.search("hill")
        assert page.is_row_present()

    def test_search_manufacturer(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.search("Sydney Tea Shop Pvt Ltd")
        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.set_entries_per_page(25)
        assert page.is_row_present()

    def test_pagination(self, setup):
        page = SAVariantListPage(setup)
        page.goto_page()
        page.click_next()
        assert page.is_row_present()

        page.click_previous()
        assert page.is_row_present()
