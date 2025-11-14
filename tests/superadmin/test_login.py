def test_superadmin_login(login_superadmin):
    driver = login_superadmin
    assert "DigiTathya" in driver.title, "Super Admin login failed!"
