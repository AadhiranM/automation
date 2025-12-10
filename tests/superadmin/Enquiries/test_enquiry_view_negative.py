import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage

@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryViewNegative:

    def test_view_without_valid_search(self, setup):
        page = SAEnquiryListPage(setup)

        # Search something that will never appear
        page.search("_____INVALID_____%$#")

        # Expect: NO rows present
        assert not page.is_row_present(), "Unexpected row present for invalid search."

        # Expect: Action menu cannot be clicked
        with pytest.raises(Exception):
            page.open_action_menu()
