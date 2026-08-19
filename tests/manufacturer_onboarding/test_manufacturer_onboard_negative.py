import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.manufacturer_onboarding.business_info_page import BusinessInfoPage
from pages.manufacturer_onboarding.kyc_page import KYCPage
from pages.manufacturer_onboarding.upload_documents_page import UploadDocumentsPage


@pytest.mark.onboarding
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerOnboardNegative:

    def test_business_info_empty_submit_shows_validation(self, setup):
        """
        Click 'Continue to KYC Verification' without filling anything.
        Expect field-level validation messages (Company name, Business
        email, Date of Incorporation, PAN, GSTIN, Turnover, Website).
        """
        business = BusinessInfoPage(setup)

        business.goto_page()
        business.wait_for_page()

        business.click_next()  # clicking Continue with everything empty

        WebDriverWait(setup, 5).until(
            lambda d: len(business.get_all_field_errors()) > 0
        )

        errors = business.get_all_field_errors()

        assert len(errors) > 0, "Expected validation errors, got none"

        # Spot-check a couple of the exact messages seen in the UI
        assert any("Company name is required" in e for e in errors)
        assert any("valid Business email" in e for e in errors)

    def test_kyc_empty_submit_shows_validation_and_toast(self, setup):
        """
        Go directly to KYC tab (bypassing Business Info) and click
        'Continue to Upload Documents' without filling anything.
        Expect a toast ("Please complete the Personal KYC before
        continuing.") AND field-level validation messages.
        """
        business = BusinessInfoPage(setup)
        kyc = KYCPage(setup)

        business.goto_page()          # land on the onboarding page first
        business.wait_for_page()

        kyc.goto_kyc_tab()             # THEN click the KYC tab
        kyc.wait_for_page()

        kyc.click_next()  # clicking Continue with everything empty

        WebDriverWait(setup, 5).until(
            lambda d: len(kyc.get_all_field_errors()) > 0
        )

        toast_text = kyc.get_toast_message()
        assert "complete the Personal KYC" in toast_text

        errors = kyc.get_all_field_errors()

        assert len(errors) > 0, "Expected validation errors, got none"
        assert any("Full name is required" in e for e in errors)
        assert any("Mobile no. is required" in e for e in errors)

    def test_upload_documents_empty_submit_shows_toast_only(self, setup):
        """
        Go directly to Upload Document tab and click Submit without
        choosing any files. This tab has NO field-level validation --
        only a toast is shown, so we must catch it immediately.
        """
        business = BusinessInfoPage(setup)
        upload = UploadDocumentsPage(setup)

        business.goto_page()          # land on the onboarding page first
        business.wait_for_page()

        upload.goto_upload_tab()       # THEN click the Upload Document tab
        upload.wait_for_page()

        upload.click_submit_only()  # clicking Submit with no files chosen

        toast_text = upload.get_toast_message()
        assert "complete valid Business Info" in toast_text