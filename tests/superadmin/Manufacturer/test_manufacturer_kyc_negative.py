import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_kyc_page import KYCPage

@pytest.mark.manufacturer
class TestKYCNegative:

    def test_without_mobile_otp(self, setup):
        page = KYCPage(setup)
        page.fill_kyc("Manikandan A", "9876543210")
        page.go_next()

        assert "kyc" in setup.current_url