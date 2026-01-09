import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_kyc_page import KYCPage

@pytest.mark.manufacturer
class TestKYCPositive:

    def test_kyc_success(self, setup):
        page = KYCPage(setup)
        page.fill_kyc("Manikandan A", "9876543210")
        page.verify_mobile_otp("123456")
        page.go_next()

        assert "upload" in setup.current_url
