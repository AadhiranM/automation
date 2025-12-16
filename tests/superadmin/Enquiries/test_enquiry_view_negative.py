import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage

@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryViewNegative:

    def test_view_without_valid_search(self, setup):
        page = SAEnquiryListPage(setup)

        # Must load Enquiries page
        page.goto_page()

        # Search something that will never appear
        page.search("%$#")

        # Expect: NO rows present
        assert page.has_no_results(), "Expected no matching results!"
