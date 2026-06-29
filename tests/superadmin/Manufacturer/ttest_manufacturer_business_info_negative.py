import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_business_info_page import BusinessInfoPage

@pytest.mark.manufacturer
class TestBusinessInfoNegative:

    def test_next_without_otp(self, setup):
        page = BusinessInfoPage(setup)
        page.fill_basic_details("Sydney Tea Shop")
        page.go_next()

        assert "business" in setup.current_url
