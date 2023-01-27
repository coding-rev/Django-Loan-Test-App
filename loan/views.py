# Python/django imports
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse

# Local app imports
from .serializers import *
from .models.loan_model import Loan
from .models.country_model import Country
from .models.sector_model import Sector
from .utils.excel_generator import generate_excel


class LoanView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = LoanSerializer

    def get(self, request):
        loans = Loan.objects.select_related("country", "sector").iterator(chunk_size=50)
        data = self.serializer_class(loans, many=True)
        return Response(data.data)


class CountryView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.iterator(chunk_size=50)
        serialized_data = self.serializer_class(countries, many=True)
        return Response(serialized_data.data)


class SectorView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = SectorSerializer

    def get(self, request):
        sectors = Sector.objects.iterator(chunk_size=50)
        serialized_data = self.serializer_class(sectors, many=True)
        return Response(serialized_data.data)


class GenerateExcelView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]

    def get(self, request):
        output_file = generate_excel()
        # Set up the Http response.
        filename = "loan_excel.xlsx"
        response = HttpResponse(
            output_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response
