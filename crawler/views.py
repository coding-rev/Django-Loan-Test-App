from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from .models import Loan


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
        countries = Loan.objects.values_list("country", flat=True)
        data = self.serializer_class(countries, many=True)
        return Response(data.data)


class LoansSectorsView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]
    serializer_class = LoanSectorSerializer

    def get(self, request):
        sectors = Loan.objects.values_list("sector", flat=True)
        data = self.serializer_class(sectors, many=True)
        return Response(data.data)
