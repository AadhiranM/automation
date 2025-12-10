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
        assert page.is_row_present(), "Expected at least 1 row for valid name search."

    def test_search_by_valid_email(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("gmail")
        assert page.is_row_present(), "Expected rows for valid email search."

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

    def test_filter_panel_created_date(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_panel_created_at(start, end)

        # ⭐ CLOSE PANEL HERE
        page.close_filter_panel()

        rows = page.get_all_created_dates()
        assert len(rows) > 0
        for r in rows:
            assert start <= r <= end

    def test_clear_panel_filters(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.open_filter_panel()
        page.click(page.CLEAR_BTN)

        # ⭐ CLOSE PANEL HERE
        page.close_filter_panel()

        assert page.is_row_present()

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
