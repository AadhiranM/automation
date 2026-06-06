import pytest
from datetime import date, timedelta

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)
from pages.superadmin.Enquiries.sa_enquiry_view_page import (
    SAEnquiryViewPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryListPositive:

    def test_search_by_valid_name(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        expected_name = page.search_first_enquiry_name()

        assert page.is_row_present()
        assert expected_name.lower() in page.get_first_row_name().lower()

    def test_search_by_valid_email(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        expected_email = page.search_first_enquiry_email()

        assert page.is_row_present()
        email = page.search_first_enquiry_email()

        assert page.verify_search_result(email)

    def test_filter_status_rejected(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.filter_by_status("Rejected")

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    def test_entries_per_page_25(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.set_entries_per_page(25)

        assert page.is_row_present()

    def test_pagination_next_previous(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.click_next()

        assert page.is_row_present()

        page.click_previous()

        assert page.is_row_present()

    def test_goto_specific_page(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.go_to_page(2)

        assert page.is_row_present()

    def test_filter_created_date(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=30)
        end = date.today()

        page.filter_by_date(
            start,
            end
        )

        rows = page.get_all_created_dates()

        if rows:

            for row_date in rows:
                assert start <= row_date <= end

    def test_view_enquiry_from_list(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.open_first_row_actions()
        page.click_view()

        view = SAEnquiryViewPage(setup)

        assert view.is_visible(view.EMAIL)
        assert view.is_visible(view.MESSAGE)
        assert view.is_visible(view.STATUS)

    def test_panel_filter_email(self, setup):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        email = page.get_first_row_email()

        page.panel_filter_by_email(
            email
        )

        assert (
                email.lower()
                in
                page.get_first_row_email().lower()
        )

    def test_panel_filter_company(
            self,
            setup
    ):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        company = page.get_first_row_company()

        page.panel_filter_by_company(
            company
        )

        assert (
                company.lower()
                in
                page.get_first_row_company().lower()
        )

    def test_panel_filter_name(
            self,
            setup
    ):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        name = page.get_first_row_name()

        page.panel_filter_by_name(
            name
        )

        assert (
                name.lower()
                in
                page.get_first_row_name().lower()
        )

    def test_panel_filter_status(self, setup):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        selected_status = page.panel_filter_select_first_status()

        assert (
                page.is_row_present()
                or page.has_no_data()
        )

        print(f"Selected Status : {selected_status}")
    def test_panel_filter_date(
            self,
            setup
    ):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        start = (
                date.today()
                -
                timedelta(days=30)
        )

        end = date.today()

        page.panel_filter_by_date(
            start,
            end
        )

        rows = page.get_all_created_dates()

        if rows:

            for row in rows:
                assert (
                        start
                        <=
                        row
                        <=
                        end
                )

    def test_panel_clear_filter(
            self,
            setup
    ):

        page = SAEnquiryListPage(setup)

        page.goto_page()

        page.open_filter_panel()

        page.click(
            page.CLEAR_FILTER_BTN
        )

        assert page.is_row_present()