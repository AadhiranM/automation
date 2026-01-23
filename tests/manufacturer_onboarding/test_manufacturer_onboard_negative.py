import pytest
import os
from selenium.webdriver.common.by import By
from pages.manufacturer_onboarding.business_info_page import BusinessInfoPage
from pages.manufacturer_onboarding.kyc_page import KYCPage
from pages.manufacturer_onboarding.upload_documents_page import UploadDocumentsPage


@pytest.mark.onboarding
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerOnboardNegative:

    # =====================================================
    # BUSINESS INFO – NEGATIVE
    # =====================================================

    def test_company_name_less_than_3_chars(self, setup):
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()

        business.fill_company_name("dd")
        business.click_next()

        assert business.get_company_name_error() == \
            "Company name must be at least 3 characters long."

    def test_company_name_special_characters(self, setup):
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()

        business.fill_company_name("@@@@")
        business.click_next()

        assert business.get_company_name_error() == \
            "Company name can only contain letters, numbers, spaces, dots, apostrophes, and hyphens."

    # =====================================================
    # KYC – NEGATIVE (INVALID PAN)
    # =====================================================

    def test_kyc_invalid_pan_format(self, setup):
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()
        business.click_next()

        kyc = KYCPage(setup)
        kyc.wait_for_page()

        kyc.fill_dob("13-01-2009")
        kyc.fill_full_name("John")
        kyc.fill_personal_pan("12345")  # invalid PAN

        kyc.click_next()

        # ✅ ASSERT VALIDATION ONLY
        assert kyc.has_any_validation_error(), \
            "Expected PAN validation error for invalid PAN"

    # =====================================================
    # UPLOAD DOCUMENTS – NEGATIVE
    # =====================================================

    def test_upload_invalid_file_type(self, setup):
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()

        setup.find_element(By.XPATH, "//a[normalize-space()='Upload Document']").click()

        upload = UploadDocumentsPage(setup)
        upload.wait_for_page()

        file_path = r"C:\Users\Manikandan A\Downloads\Digitathya\textfile.txt"
        assert os.path.exists(file_path)

        # 🔥 Upload invalid file
        upload.upload_business_pan(file_path)

        # ✅ ASSERT IMMEDIATE INLINE VALIDATION (NO SUBMIT)
        assert upload.get_business_pan_error() == "Invalid file type."


