from django.urls import path, include
from .views import *

app_name = "crawler"

urlpatterns = [
    path("loans", LoansView.as_view()),
    path("countries", LoansCountriesView.as_view()),
    path("sectors", LoansSectorsView.as_view())
]
