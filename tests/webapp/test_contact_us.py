# File: tests/webapp/test_contact_us.py

import pytest
from pages.webapp.contact_us_page import ContactUsPage


@pytest.mark.webapp
class TestContactUs:

    # -------------------------------------------------------
    # POSITIVE TEST - VALID FORM SUBMISSION
    # Smoke + Sanity + Regression
    # -------------------------------------------------------
    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_submit_valid_enquiry(self, setup):
        page = ContactUsPage(setup)

        page.open()

        page.fill_form(
            name="Manikandan A",
            phone="9876543210",
            email="mani@mailinator.com",
            company="Digitathya Pvt Ltd",
            message="Testing enquiry automation flow"
        )

        page.submit()

        msg = page.get_success_message()

        assert (
            "success" in msg.lower()
            or
            "thank" in msg.lower()
        )

    # -------------------------------------------------------
    # NEGATIVE TEST – INVALID EMAIL
    # Sanity + Regression
    # -------------------------------------------------------
    @pytest.mark.sanity
    @pytest.mark.parametrize(
        "email",
        [
            "test",
            "abc@"
        ]
    )
    def test_invalid_email(self, setup, email):
        page = ContactUsPage(setup)

        page.open()

        page.fill_form(
            name="Test User",
            phone="9876543210",
            email=email,
            company="Dummy",
            message="Testing"
        )

        page.submit()

        assert not page.is_success_message_displayed(), \
            "Success message displayed for invalid email"

    # -------------------------------------------------------
    # NEGATIVE TEST – INVALID PHONE NUMBER
    # Sanity + Regression
    # -------------------------------------------------------
    @pytest.mark.sanity
    @pytest.mark.parametrize(
        "phone",
        [
            "9876543"
        ]
    )
    def test_invalid_phone(self, setup, phone):
        page = ContactUsPage(setup)

        page.open()

        page.fill_form(
            "Test User",
            phone,
            "valid@test.com",
            "Dummy",
            "Testing"
        )

        page.submit()

        assert not page.is_success_message_displayed(), \
            "Success message displayed for invalid phone"

    # -------------------------------------------------------
    # NEGATIVE TEST – REQUIRED FIELD BLANK
    # Regression Only
    # -------------------------------------------------------
    @pytest.mark.parametrize(
        "field",
        [
            "name",
            "phone",
            "email",
            "message"
        ]
    )
    def test_blank_required_fields(self, setup, field):
        page = ContactUsPage(setup)

        page.open()

        data = {
            "name": "Test",
            "phone": "9876543210",
            "email": "valid@test.com",
            "company": "Digitathya",
            "message": "Hello"
        }

        data[field] = ""

        page.fill_form(
            data["name"],
            data["phone"],
            data["email"],
            data["company"],
            data["message"]
        )

        page.submit()

        assert not page.is_success_message_displayed(), \
            f"Success message displayed when {field} is blank"