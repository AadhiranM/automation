import pytest
from pages.superadmin.Login.sa_login_page import SuperAdminLoginPage


@pytest.mark.superadmin
class TestSuperAdminLogin:

    LOGIN_URL = "https://beta.digitathya.com/admin/login"

    # ============================================================
    # 🔵 UI VALIDATIONS — Button Enable/Disable Logic
    # ============================================================
    def test_login_button_disabled_on_load(self, setup):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        assert not page.is_login_button_enabled(), \
            "Login button must be disabled on first load"

    def test_login_button_disabled_with_only_email(self, setup):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        page.enter_email("dummy@mail.com")

        assert not page.is_login_button_enabled(), \
            "Login button must remain disabled with only email entered"

    def test_login_button_disabled_with_only_password(self, setup):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        page.enter_password("DummyPass123")

        assert not page.is_login_button_enabled(), \
            "Login button must remain disabled with only password entered"

    def test_login_button_enabled_when_both_fields_entered(self, setup):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        page.enter_email("dummy@mail.com")
        page.enter_password("DummyPass123")

        assert page.is_login_button_enabled(), \
            "Login button should be enabled only after both fields are entered"

    # ============================================================
    # 🔵 POSITIVE LOGIN
    # ============================================================
    def test_valid_login(self, setup, get_config):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        creds = get_config["users"]["superadmin"]

        page.login(creds["username"], creds["password"])

        assert page.is_dashboard_loaded(), \
            "Dashboard did NOT load after valid login"

    # ============================================================
    # 🔵 NEGATIVE LOGIN — Wrong Password
    # ============================================================
    def test_invalid_password(self, setup, get_config):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        creds = get_config["users"]["superadmin"]

        page.login(creds["username"], "WrongPassword123")

        assert "invalid" in page.get_error_message().lower(), \
            "Error message for invalid password not shown"

    # ============================================================
    # 🔵 NEGATIVE LOGIN — Wrong Email + Wrong Password
    # ============================================================
    def test_invalid_email_and_password(self, setup):
        page = SuperAdminLoginPage(setup)
        page.open(self.LOGIN_URL)

        page.login("unknown@mail.com", "InvalidPass")

        assert "invalid" in page.get_error_message().lower(), \
            "Invalid credentials error NOT shown"
