from django.urls import path, include
from . import views

app_name = "loan"

urlpatterns = [
    path("loans", views.LoansView.as_view()),
    path("countries", views.CountryView.as_view()),
    path("sectors", views.SectorView.as_view()),
    path("excel", views.GenerateExcelView.as_view()),
]
