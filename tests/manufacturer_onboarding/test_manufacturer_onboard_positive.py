import pytest
from pages.manufacturer_onboarding.business_info_page import BusinessInfoPage
from pages.manufacturer_onboarding.kyc_page import KYCPage
from pages.manufacturer_onboarding.upload_documents_page import UploadDocumentsPage
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)
from utilities.data_generator import (
    generate_manufacturer_name,
    generate_mailinator_email
)


@pytest.mark.onboarding
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerOnboardPositive:

    def test_business_info_positive(self, setup):

        # ================= BUSINESS INFO =================

        business = BusinessInfoPage(setup)

        business.goto_page()
        business.wait_for_page()

        company_name = generate_manufacturer_name()
        email = generate_mailinator_email()

        business.fill_company_name(company_name)
        business.fill_business_email(email)

        business.fill_date_of_incorporation(
            "01-06-1980"
        )

        business.select_business_type()
        business.select_industry()

        business.fill_gst(
            "22AAAAA0000A1Z5"
        )

        business.fill_pan(
            "PQRST6789K"
        )

        business.fill_website(
            "https://technova.com"
        )

        business.select_annual_turnover()

        business.click_next()

        print(f"Company Name : {company_name}")
        print(f"Email        : {email}")

        # ================= KYC =================

        kyc = KYCPage(setup)

        kyc.wait_for_page()

        kyc.select_director_dob(
            "10-10-1985"
        )

        kyc.fill_director_name(
            "John Smith"
        )

        kyc.fill_director_pan(
            "PQRST6789K"
        )

        kyc.fill_director_driving_license(
            "TN6378997789123"
        )

        kyc.fill_address(
            "chennai"
        )

        kyc.fill_mobile(
            "9538745383"
        )

        kyc.click_next()

        # ================= UPLOAD DOCUMENTS =================

        upload = UploadDocumentsPage(setup)

        upload.wait_for_page()

        upload.upload_business_pan(
            r"C:/Users/Manikandan A/Downloads/Digitathya/Business PAN.pdf"
        )

        upload.upload_certificate(
            r"C:/Users/Manikandan A/Downloads/Digitathya/Certificate of Incorporation.pdf"
        )

        upload.upload_moa(
            r"C:/Users/Manikandan A/Downloads/Digitathya/Memorandum of Association.pdf"
        )

        upload.upload_board_resolution(
            r"C:/Users/Manikandan A/Downloads/Digitathya/Board Resolution.pdf"
        )


        upload.verify_all_files_selected()

        upload.wait_for_upload_processing()

        upload.submit()


        # ================= VERIFY IN MANUFACTURER LIST =================

        list_page = SAManufacturerListPage(setup)

        list_page.goto_page()

        list_page.search(company_name)

        assert list_page.is_company_present(company_name), \
            f"Expected manufacturer '{company_name}' not found in Manufacturer List"

        print(
            f"✅ Manufacturer created successfully: {company_name}"
        )