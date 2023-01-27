from django.urls import path, include
from . import views

app_name = "loan"

urlpatterns = [
    path("loans", views.LoanView.as_view(), name="loan_path"),
    path("countries", views.CountryView.as_view(), name="country_path"),
    path("sectors", views.SectorView.as_view(), name="sector_path"),
    path("excel", views.GenerateExcelView.as_view(), name="generate_excel_path"),
]
