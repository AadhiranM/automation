# File: tests/webapp/test_contact_us.py

import pytest
from pages.webapp.contact_us_page import ContactUsPage


@pytest.mark.webapp
class TestContactUs:

    # -------------------------------------------------------
    # POSITIVE TEST - VALID FORM SUBMISSION
    # -------------------------------------------------------
    def test_submit_valid_enquiry(self, setup):
        page = ContactUsPage(setup)
        page.open()   # CORRECT

        page.fill_form(
            name="Manikandan A",
            phone="9876543210",
            email="mani@test.com",
            company="Digitathya Pvt Ltd",
            message="Testing enquiry automation flow"
        )

        page.submit()

        # Validate success message
        msg = page.get_success_message()
        assert ("success" in msg.lower() or "thank" in msg.lower()), \
            "Success message not found after valid form submission"

    # -------------------------------------------------------
    # NEGATIVE TEST – INVALID EMAIL
    # -------------------------------------------------------
    @pytest.mark.parametrize("email", [
        "test", "abc@", "abc@gmail", "@gmail.com", "mani@.com"
    ])
    def test_invalid_email(self, setup, email):
        page = ContactUsPage(setup)
        page.open()   # CORRECT

        page.fill_form(
            name="Test User",
            phone="9876543210",
            email=email,
            company="Dummy",
            message="Test"
        )

        page.submit()

        # Expect success message NOT to appear
        with pytest.raises(Exception):
            page.get_success_message()

    # -------------------------------------------------------
    # NEGATIVE TEST – INVALID PHONE NUMBER
    # -------------------------------------------------------
    @pytest.mark.parametrize("phone", [
        "12345", "1111111111", "abc1234567", "!@#4567890", "9876543"
    ])
    def test_invalid_phone(self, setup, phone):
        page = ContactUsPage(setup)
        page.open()   # CORRECT

        page.fill_form(
            name="Test User",
            phone=phone,
            email="valid@test.com",
            company="Dummy",
            message="Test message"
        )

        page.submit()

        # Expect success message NOT to appear
        with pytest.raises(Exception):
            page.get_success_message()

    # -------------------------------------------------------
    # NEGATIVE TEST – REQUIRED FIELD BLANK
    # -------------------------------------------------------
    @pytest.mark.parametrize("field", ["name", "phone", "email", "message"])
    def test_blank_required_fields(self, setup, field):

        page = ContactUsPage(setup)
        page.open()   # CORRECT

        data = {
            "name": "Test",
            "phone": "9876543210",
            "email": "valid@test.com",
            "company": "Digitathya",
            "message": "Hello"
        }

        # make one field blank
        data[field] = ""

        page.fill_form(
            data["name"],
            data["phone"],
            data["email"],
            data["company"],
            data["message"]
        )

        page.submit()

        # Expect success message NOT to appear
        with pytest.raises(Exception):
            page.get_success_message()
