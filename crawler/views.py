from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from .models import Loan
from .excel_generator import generate_excel


class LoansView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = LoanSerializer

    def get(self, request):
        loans = Loan.objects.iterator(chunk_size=50)
        data = self.serializer_class(loans, many=True)
        return Response(data.data)


class LoansCountriesView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = LoanCountrySerializer

    def get(self, request):
        loans = Loan.objects.iterator(chunk_size=50)
        country_data = self.serializer_class(loans, many=True)
        return Response(country_data.data)


class LoansSectorsView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = LoanSectorSerializer

    def get(self, request):
        loans = Loan.objects.iterator(chunk_size=50)
        sector_data = self.serializer_class(loans, many=True)
        return Response(sector_data.data)


class GenerateExcelView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]

    def get(self, request):
        output = generate_excel()
        # Set up the Http response.
        filename = "loan_excel.xlsx"
        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=%s" % filename

        return response
