import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.Manufacturer.sa_manufacturer_invite_page import (
    SAManufacturerInvitePage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerInviteNegative:

    def test_cancel_invite(self, setup):

        list_page = SAManufacturerListPage(setup)

        invite_page = SAManufacturerInvitePage(setup)

        list_page.goto_page()

        manufacturer_name = (
            list_page.get_first_row_company_name()
        )

        print(
            f"Cancelling invite for: {manufacturer_name}"
        )

        list_page.open_first_row_actions()

        list_page.click_send_invite()

        invite_page.cancel_send()

        assert invite_page.is_confirmation_closed(), \
            "Confirmation popup still visible after clicking Cancel"