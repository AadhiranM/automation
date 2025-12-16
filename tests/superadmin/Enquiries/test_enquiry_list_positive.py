import pytest
from datetime import date, timedelta
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryListPositive:

    def test_search_by_valid_name(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("test")
        assert page.is_row_present()

    def test_search_by_valid_email(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("gmail")
        assert page.is_row_present()

    def test_filter_status_rejected(self, setup):
        """Verify Status dropdown works."""
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.filter_by_status("Rejected")
        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        """Verify entries per page works."""
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.set_entries_per_page("25")
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

        page.go_to_page("2")
        assert page.is_row_present()

    def test_filter_inline_created_date(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=3)
        end = date.today()

        page.filter_inline_created_at(start, end)
        rows = page.get_all_created_dates()
        assert len(rows) > 0
        for r in rows:
            assert start <= r <= end

    def test_view_enquiry_from_list(self, setup):
        from pages.superadmin.Enquiries.sa_enquiry_view_page import SAEnquiryViewPage

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("test")
        page.open_action_menu()
        page.click_view()

        view = SAEnquiryViewPage(setup)
        assert view.is_visible(view.EMAIL)
        assert view.is_visible(view.MESSAGE)
        assert view.is_visible(view.STATUS)
