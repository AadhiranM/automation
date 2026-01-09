import pytest
from pages.manufacturer_onboarding.business_info_page import BusinessInfoPage
from pages.manufacturer_onboarding.kyc_page import KYCPage
from pages.manufacturer_onboarding.upload_documents_page import UploadDocumentsPage


@pytest.mark.onboarding
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerOnboardNegative:
    """
    NEGATIVE: Full Manufacturer Onboarding Flow
    """

    # ---------------- BUSINESS INFO ----------------

    def test_negative_business_info_empty_form(self, setup):
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()

        business.click_next()
        assert business.is_error_visible()

    def test_negative_business_info_invalid_email(self, setup):
        business = BusinessInfoPage(setup)
        business.wait_for_page()

        business.fill_company_name("Test Company")
        business.fill_business_email("invalid@")

        business.click_next()
        assert business.is_error_visible()

    def test_negative_business_info_future_date(self, setup):
        business = BusinessInfoPage(setup)
        business.wait_for_page()

        business.fill_company_name("Test Company")
        business.fill_business_email("test@mailinator.com")
        business.fill_date_of_incorporation("01-01-2090")

        business.click_next()
        assert business.is_error_visible()

    # ---------------- KYC ----------------

    def test_negative_kyc_empty_form(self, setup):
        kyc = KYCPage(setup)
        kyc.wait_for_page()

        kyc.click_next()
        assert kyc.is_error_visible()

    def test_negative_kyc_invalid_pan(self, setup):
        kyc = KYCPage(setup)
        kyc.wait_for_page()

        kyc.fill_director_name("John")
        kyc.fill_director_pan("1234ABCDE")  # ❌ invalid PAN

        kyc.click_next()
        assert kyc.is_error_visible()

    # ---------------- UPLOAD DOCUMENTS ----------------

    def test_negative_upload_documents_no_files(self, setup):
        upload = UploadDocumentsPage(setup)
        upload.wait_for_page()

        upload.submit()
        assert upload.is_error_visible()

    def test_negative_upload_invalid_file_type(self, setup):
        upload = UploadDocumentsPage(setup)
        upload.wait_for_page()

        upload.upload_business_pan("tests/data/invalid.txt")  # ❌ invalid format
        upload.submit()

        assert upload.is_error_visible()
