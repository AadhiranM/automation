import pytest
from pages.manufacturer_onboarding.business_info_page import BusinessInfoPage
from pages.manufacturer_onboarding.kyc_page import KYCPage
from pages.manufacturer_onboarding.upload_documents_page import UploadDocumentsPage


@pytest.mark.onboarding
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerOnboardPositive:
    """
    POSITIVE: Full Manufacturer Onboarding Flow
    Business Info ➜ KYC ➜ Upload Documents
    """

    def test_full_onboarding_positive_flow(self, setup):
        # ================= BUSINESS INFO =================
        business = BusinessInfoPage(setup)
        business.goto_page()
        business.wait_for_page()

        business.fill_company_name("Sydney Tea Shop Pvt Ltd")
        business.fill_business_email("sydney@mailinator.com")
        business.fill_date_of_incorporation("01-06-1980")

        business.select_business_type("Private Limited Company")
        business.select_industry("Aerospace")

        business.fill_gst("22AAAAA0000A1Z5")
        business.fill_pan("PQRST6789K")
        business.fill_website("https://sydneytea.com")

        business.select_annual_turnover("1 Lakh - 10 Lakhs")
        business.click_next()

        assert not business.is_error_visible()

        # ================= KYC =================
        kyc = KYCPage(setup)
        kyc.wait_for_page()

        kyc.select_director_dob("10-10-1985")
        kyc.fill_director_name("John Smith")
        kyc.fill_director_driving_license("TN6378997789123")
        kyc.fill_director_pan("PQRST6789K")
        kyc.fill_address("chennai")
        kyc.fill_mobile("9876543210")


        kyc.click_next()
        assert not kyc.is_error_visible()

        # ================= UPLOAD DOCUMENTS =================
        upload = UploadDocumentsPage(setup)
        upload.wait_for_page()

        upload.upload_business_pan(
            "C:/Users/Manikandan A/Downloads/Digitathya/Business PAN.pdf"
        )
        upload.upload_certificate(
            "C:/Users/Manikandan A/Downloads/Digitathya/Certificate of Incorporation.pdf"
        )
        upload.upload_moa(
            "C:/Users/Manikandan A/Downloads/Digitathya/Memorandum of Association.pdf"
        )
        upload.upload_board_resolution(
            "C:/Users/Manikandan A/Downloads/Digitathya/Board Resolution.pdf"
        )

        upload.submit()
        assert upload.is_success_message_visible()
