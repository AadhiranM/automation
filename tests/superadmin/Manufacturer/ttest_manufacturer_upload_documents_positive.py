import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_upload_documents_page import UploadDocumentsPage

@pytest.mark.manufacturer
class TestUploadDocumentsPositive:

    def test_upload_success(self, setup):
        page = UploadDocumentsPage(setup)
        page.upload_pan("tests/data/pan.png")
        page.submit()

        assert "verification-inprogress" in setup.current_url

