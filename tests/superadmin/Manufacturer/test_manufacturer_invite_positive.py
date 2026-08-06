import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.Manufacturer.sa_manufacturer_invite_page import (
    SAManufacturerInvitePage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerInvitePositive:

    @pytest.mark.sanity
    def test_send_invite_success(self, setup):

        list_page = SAManufacturerListPage(setup)

        invite_page = SAManufacturerInvitePage(setup)

        list_page.goto_page()

        # Capture first row manufacturer name
        manufacturer_name = (
            list_page.get_first_row_company_name()
        )

        print(
            f"Sending invite to: {manufacturer_name}"
        )

        # Open first row action menu
        list_page.open_first_row_actions()

        # Click Send Invite
        list_page.click_send_invite()

        # Confirm invite
        invite_page.invite_manufacturer()

        print(
            f" Invite sent successfully for: "
            f"{manufacturer_name}"
        )