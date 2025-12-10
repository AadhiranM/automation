import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_edit_page import SAEnquiryEditPage


@pytest.mark.superadmin
class TestEnquiryEditNegative:

    def test_submit_disabled_without_change(self, setup):
        list_page = SAEnquiryListPage(setup)

        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_edit()

        edit = SAEnquiryEditPage(setup)

        # Capture original status
        original_status = edit.get_current_status()

        # Button should stay disabled
        assert not edit.is_submit_enabled(), "Submit should stay disabled if no change is made."

        # Try clicking (should do nothing)
        try:
            edit.click_save()
        except:
            pass

        # Status must remain same
        assert edit.get_current_status() == original_status, \
            "Status changed without selecting a new value!"

        print("✔ Negative: Submit disabled without any change.")
