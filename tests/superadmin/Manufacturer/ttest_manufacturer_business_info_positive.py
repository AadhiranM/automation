import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_business_info_page import BusinessInfoPage

@pytest.mark.manufacturer
class TestBusinessInfoPositive:

    def test_business_info_success(self, setup):
        page = BusinessInfoPage(setup)

        page.fill_basic_details("Sydney Tea Shop")
        page.send_and_verify_otp("123456")
        page.go_next()

        assert "kyc" in setup.current_url