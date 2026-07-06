from datetime import date, timedelta

import pytest
from pages.superadmin.Reports.sa_download_reports_page import (
    SADownloadReportsPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestDownloadReports:

    # ==========================================
    # SEARCH
    # ==========================================
    def test_search_report(self, setup):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        report_name = page.search_report()

        assert report_name != ""

    # ==========================================
    # DATE FILTER
    # ==========================================
    def test_filter_date_range(self, setup):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_date(start, end)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==========================================
    # FORMAT FILTER
    # ==========================================
    @pytest.mark.parametrize(
        "file_format",
        [
            "CSV",
            "XLSX"
        ]
    )
    def test_filter_by_format(
        self,
        setup,
        file_format
    ):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        page.filter_by_format(file_format)

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================================
    # STATUS FILTER
    # ==========================================
    @pytest.mark.parametrize(
        "status",
        [
            "Completed",
            "Pending"
        ]
    )
    def test_filter_by_status(
        self,
        setup,
        status
    ):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        page.filter_by_status(status)

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================================
    # ENTRIES
    # ==========================================
    def test_entries_per_page_25(self, setup):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        page.set_entries_per_page("25")

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================================
    # PAGINATION
    # ==========================================
    def test_next_previous_page(self, setup):
        page = SADownloadReportsPage(setup)

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
        page = SADownloadReportsPage(setup)

        page.goto_page()

        page.go_to_page("2")

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================================
    # DOWNLOAD
    # ==========================================
    def test_download_first_report(self, setup):
        page = SADownloadReportsPage(setup)

        page.goto_page()

        result = page.download_first_report()

        assert result in ["DOWNLOADED", "NO_DATA"]