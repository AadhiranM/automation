import pytest
from datetime import date, timedelta
from pages.superadmin.QRManagement.sa_product_list_page import SAProductListPage
from utilities.flatpickr import FlatpickrRangePicker


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestProductListPositive:

    @pytest.mark.sanity
    def test_search_product(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()

        product = page.get_first_product_name()

        page.search(product)

        assert page.get_first_product_name() == product

    @pytest.mark.sanity
    def test_filter_status_active(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()
        page.filter_by_status("Active")
        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()
        page.set_entries_per_page("25")
        assert page.is_row_present()

    def test_pagination(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()
        page.click_next()
        assert page.is_row_present()
        page.click_previous()
        assert page.is_row_present()

    def test_go_to_page(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()
        page.go_to_page("2")
        assert page.is_row_present()



    def test_filter_created_date(self, setup):
        page = SAProductListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_created_date(start, end)

        rows = page.get_created_dates()

        if not rows:
            pytest.skip("No data for selected range")

        # FIX: sort issue safety
        for d in rows:
            assert start <= d <= end, f"Date {d} not in range {start} - {end}"