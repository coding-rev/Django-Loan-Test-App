from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from .models import Loan
from .excel_generator import generate_excel
from django.http import JsonResponse


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

    def get(self, request):
        country = Loan.objects.all().values_list("country", flat=True)
        return JsonResponse({"countries": list(country)})


class LoansSectorsView(generics.GenericAPIView):
    """Provide Retrieve functionality"""

    permission_classes = [AllowAny]

    def get(self, request):
        sectors = Loan.objects.all().values_list("sector", flat=True)
        return JsonResponse({"sectors": list(sectors)})


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
