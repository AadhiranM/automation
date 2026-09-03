import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_assign_page import (
    SAEnquiryAssignPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryAssignNegative:

    @pytest.mark.sanity
    def test_assign_internal_user_empty_submit(self, setup):

        print("=" * 60)
        print("NEGATIVE ASSIGN INTERNAL USER TEST")
        print("=" * 60)

        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        # --------------------------------------------
        # Open Enquiries
        # --------------------------------------------

        list_page.goto_page()

        # --------------------------------------------
        # Open Action menu
        # --------------------------------------------

        assign_page.open_actions()

        # --------------------------------------------
        # Click Assign Internal User
        # --------------------------------------------

        assign_page.click(
            assign_page.ASSIGN_INTERNAL_USER
        )

        print("Assign Internal User popup opened")

        # --------------------------------------------
        # Wait for popup
        # --------------------------------------------

        wait = WebDriverWait(setup, 15)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "assignInternalUserModal")
            )
        )

        # --------------------------------------------
        # DO NOT SELECT ANY INTERNAL USER
        # --------------------------------------------

        print("No Internal User selected")

        # --------------------------------------------
        # Click Submit
        # --------------------------------------------

        assign_page.click(
            assign_page.SUBMIT_BTN
        )

        print("Submit clicked without selecting Internal User")

        # --------------------------------------------
        # Validate message
        # --------------------------------------------

        validation_message = (
            "Please select an internal user."
        )

        validation = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//div[@id='assignInternalUserModal']"
                    f"//*[normalize-space()='{validation_message}']"
                )
            )
        )

        assert validation.is_displayed()

        print(
            f"PASS: Validation message displayed - "
            f"{validation_message}"
        )