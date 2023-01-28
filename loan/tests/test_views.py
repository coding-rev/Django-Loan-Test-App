# Python/django imports
from django.test import TestCase
from django.urls import reverse

# Local apps imports
from loan.models.loan_model import Loan
from loan.models.country_model import Country
from loan.models.sector_model import Sector
from loan.models.currency_model import Currency


""" App urls/routes test class"""


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = Country.objects.create(name="Germany")
        cls.sector = Sector.objects.create(name="Credit lines")
        cls.currency = Currency.objects.create(symbol="$")
        cls.loan = Loan.objects.create(
            signature_date="2023-01-26",
            title="Test Loan Title",
            country=cls.country,
            sector=cls.sector,
            currency=cls.currency,
            signed_amount=135000000,
        )

    def test_country_view(self):
        url = reverse("loan:country_path")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sector_view(self):
        url = reverse("loan:sector_path")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_loan_view(self):
        url = reverse("loan:loan_path")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_generate_excel(self):
        url = reverse("loan:generate_excel_path")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
