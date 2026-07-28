import pytest
from datetime import date, timedelta

from pages.superadmin.QRcodemonitoring.sa_qr_monitoring_page import (
    SAQRMonitoringPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestQRMonitoring:

    # ==================================================
    # SEARCH
    # ==================================================
    def test_search_scan_id(self, setup):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.search("dummy")

        assert page.is_row_present()

    # ==================================================
    # STATUS FILTER
    # ==================================================
    @pytest.mark.parametrize(
        "status",
        [
            "All",
            "Processing",
        ]
    )
    def test_filter_status(self, setup, status):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.filter_by_status(status)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==================================================
    # DATE FILTER
    # ==================================================
    def test_filter_date_range(self, setup):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_date(start, end)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==================================================
    # ENTRIES
    # ==================================================
    def test_entries_per_page_25(self, setup):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.set_entries_per_page("25")

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==================================================
    # PAGINATION
    # ==================================================
    def test_next_previous_page(self, setup):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.click_next()

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

        page.click_previous()

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    def test_go_to_page_2(self, setup):

        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.go_to_page("2")

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==================================================
    # EXPORT
    # ==================================================
    def test_export_id_based(self, setup):
        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.export_id_based()

        page.go_to_reports_page()

        assert "reports" in page.driver.current_url.lower()

    def test_export_user_based(self, setup):
        page = SAQRMonitoringPage(setup)

        page.goto_page()

        page.click_export()

        page.export_user_based()

        assert page.driver.find_element(
            *page.EXPORT_SUCCESS
        ).is_displayed()

    def test_export_bulk_id_based(self, setup):
        page = SAQRMonitoringPage(setup)

        page.goto_page()
        page.export_bulk_id_based()
        page.go_to_reports_page()

        assert "reports" in page.driver.current_url.lower()

    def test_export_date_based(self, setup):
        page = SAQRMonitoringPage(setup)

        page.goto_page()
        page.export_date_based()
        page.go_to_reports_page()

        assert "reports" in page.driver.current_url.lower()