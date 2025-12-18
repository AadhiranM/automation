import pytest
from selenium.common.exceptions import TimeoutException
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_invite_page import SAManufacturerInvitePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerInviteNegative:

    def test_cancel_invite(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.search("frankfurt")
        page.open_action_menu()
        page.click_send_invite()

        invite = SAManufacturerInvitePage(setup)
        invite.cancel_send()

        with pytest.raises(TimeoutException):
            invite.wait_for_success()
