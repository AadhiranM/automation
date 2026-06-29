import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_login_after_accept_invite_page import ManufacturerLoginPage


@pytest.mark.manufacturer
class TestLoginWithTempPassword:

    def test_login_success(self, setup):
        login = ManufacturerLoginPage(setup)
        login.login("australia@mailinator.com", "Temp@123")

        assert "manufacturer/registration" in setup.current_url
