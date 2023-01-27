# Python/django imports
from django.test import SimpleTestCase
from django.urls import reverse, resolve
# Local apps imports
from loan import views

''' App urls/routes test class'''
class TestLoanUrls(SimpleTestCase):
    def test_loan_route(self):
        url = reverse("loan:loan_path")
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.LoanView)

    def test_country_route(self):
        url = reverse("loan:country_path")
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.CountryView)

    def test_sector_route(self):
        url = reverse("loan:sector_path")
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.SectorView)

  
    
