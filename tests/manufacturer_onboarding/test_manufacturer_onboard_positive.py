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
from pages.superadmin.Manufacturer.sa_manufacturer_service_page import (
    SAManufacturerServicePage
)
from pathlib import Path
# Project root -> automation/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_DATA = PROJECT_ROOT / "test_data" / "images"
print(f"Project Root : {PROJECT_ROOT}")
print(f"Test Data    : {TEST_DATA}")
assert TEST_DATA.exists(), f"Folder not found: {TEST_DATA}"

@pytest.mark.onboarding
@pytest.mark.smoke
@pytest.mark.sanity
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

        # File Paths
        business_pan = TEST_DATA / "Business PAN.pdf"
        certificate = TEST_DATA / "Certificate of Incorporation.pdf"
        moa = TEST_DATA / "Memorandum of Association.pdf"
        board_resolution = TEST_DATA / "Board Resolution.pdf"

        # Debug Prints
        print(f"Business PAN           : {business_pan}")
        print(f"Certificate            : {certificate}")
        print(f"MOA                    : {moa}")
        print(f"Board Resolution       : {board_resolution}")

        # Verify files exist
        assert business_pan.exists(), f"Missing file: {business_pan}"
        assert certificate.exists(), f"Missing file: {certificate}"
        assert moa.exists(), f"Missing file: {moa}"
        assert board_resolution.exists(), f"Missing file: {board_resolution}"

        # Upload files
        upload.upload_business_pan(str(business_pan))

        upload.upload_certificate(str(certificate))

        upload.upload_moa(str(moa))

        upload.upload_board_resolution(str(board_resolution))

        upload.verify_all_files_selected()

        upload.wait_for_upload_processing()

        upload.submit()

        list_page = SAManufacturerListPage(setup)

        list_page.goto_page()

        list_page.search(company_name)

        assert list_page.is_company_present(company_name)

        list_page.wait_until_status(company_name, "Approved")

        list_page.open_service_management()

        service = SAManufacturerServicePage(setup)

        assert "/manage_services" in setup.current_url

        service.check_all_services()

        assert service.all_services_checked()

        service.submit_services()

        service.click_back()

        list_page.search(company_name)

        list_page.open_service_management()

        assert service.all_services_checked()