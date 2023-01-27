# Python/django imports
from django.test import TestCase
# Local apps imports
from loan.models.loan_model import Loan
from loan.models.country_model import Country
from loan.models.sector_model import Sector

''' Loan test class'''
class TestLoanModels(TestCase):
    def test_loan_model_fields(self):
        # Create required model instances for test
        country = Country.objects.create(name="Germany")
        sector = Sector.objects.create(name="Credit lines")
        loan = Loan.objects.create(
            signature_date="2023-01-26",
            title="Test Loan Title",
            country=country,
            sector=sector,
            signed_amount="€135,000,000",
        )
        # Assertions
        self.assertTrue(Loan.objects.filter(id=loan.id).exists())
        self.assertTrue(Country.objects.filter(id=country.id).exists())
        self.assertTrue(Sector.objects.filter(id=sector.id).exists())