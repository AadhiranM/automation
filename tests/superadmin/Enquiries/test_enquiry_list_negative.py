# tests/superadmin/Enquiries/test_enquiry_list_negative.py

import pytest
from datetime import date, timedelta
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryListNegative:

    def test_search_invalid_special_characters(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()
        page.search("!@#$%^&*")
        assert page.has_no_results()


    def test_search_only_spaces(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()
        page.search("   ")
        assert page.is_row_present()


    def test_inline_filter_future_date(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        start = date.today() + timedelta(days=10)
        end   = start + timedelta(days=3)

        blocked = page.filter_inline_created_at(start, end)

        if blocked:
            # no selection happened → table unchanged
            assert page.is_row_present(), "Inline blocked selection but table unexpectedly empty."
        else:
            assert page.has_no_results(), "Inline future date should show zero results."


    def test_panel_filter_future_date(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()

        start = date.today() + timedelta(days=20)
        end   = start + timedelta(days=3)

        blocked = page.filter_panel_created_at(start, end)

        if blocked:
            assert page.is_row_present(), "Panel blocked but table changed unexpectedly."
        else:
            assert page.has_no_results(), "Panel future date should show ZERO results."


    def test_clear_panel_filter_without_applying(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()
        page.open_filter_panel()
        page.click(page.CLEAR_BTN)
        page.close_filter_panel()
        assert page.is_row_present()


    def test_previous_page_on_first_page(self, setup):
        page = SAEnquiryListPage(setup)
        page.goto_page()
        page.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            prev_btn = page.driver.find_element("xpath", "//a[contains(text(),'Previous')]")
            prev_btn.click()
        except:
            pass
        assert page.is_row_present()
