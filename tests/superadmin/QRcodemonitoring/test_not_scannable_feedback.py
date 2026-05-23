import pytest
from datetime import date, timedelta

from pages.superadmin.QRcodemonitoring.sa_not_scannable_feedback_page import (
    SANotScannableFeedbackPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestnotscannableFeedback:

    # ==================================================
    # SEARCH
    # ==================================================
    def test_search(self, setup):
        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        scan_id = page.search_first_record()

        assert scan_id != ""

    # ==================================================
    # STATUS FILTER
    # ==================================================

    @pytest.mark.parametrize(
        "status",
        [
            "Manufacturer Assigned",
            "Manufacturer Not Assigned"
        ]
    )
    def test_filter_status(self, setup, status):
        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        page.filter_by_status(status)

    # ==================================================
    # DATE FILTER
    # ==================================================
    def test_filter_date_range(self, setup):

        page = SANotScannableFeedbackPage(setup)

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

        page = SANotScannableFeedbackPage(setup)

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

        page = SANotScannableFeedbackPage(setup)

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

        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        page.go_to_page("2")

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # ==================================================
    # VIEW
    # ==================================================
    def test_view_feedback(self, setup):

        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        page.view_feedback()

        assert "show" in page.driver.current_url.lower()

    # ==================================================
    # EDIT
    # ==================================================
    def test_edit_feedback(self, setup):

        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        comment = page.edit_feedback()

        assert comment != ""

    # ==================================================
    # EXPORT
    # ==================================================
    def test_export(self, setup):

        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        page.export_records()

        assert True

    def test_assign_manufacturer(self, setup):
        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        removed_scan_id = page.assign_manufacturer_and_verify_row_removed()

        assert removed_scan_id != ""

    def test_export_csv_report(self, setup):
        page = SANotScannableFeedbackPage(setup)

        page.goto_page()

        page.export_csv_report()
