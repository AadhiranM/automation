import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_invite_page import SAManufacturerInvitePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerInvitePositive:

    def test_send_invite_success(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.search("frankfurt")
        page.open_action_menu()
        page.click_send_invite()

        invite = SAManufacturerInvitePage(setup)
        invite.confirm_send()
        invite.wait_for_success()
        invite.click_ok()
