
import pytest

from pages.superadmin.Reports.sa_generate_reports_page import (
    SAGenerateReportsPage
)


@pytest.mark.superadmin
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestGenerateReports:

    def test_manufacturer_report_csv(self, setup):
        page = SAGenerateReportsPage(setup)

        page.goto_page()

        report = page.generate_manufacturer_report(
            "Automation_Manufacturer_Report",
            "CSV",
            "Today"
        )

        assert report != ""

    def test_manufacturer_activity_report_xlsx(self, setup):
        page = SAGenerateReportsPage(setup)

        page.goto_page()

        report = page.generate_manufacturer_activity_report(
            "Automation_Manufacturer_Activity",
            "XLSX",
            "Yesterday"
        )

        assert report != ""