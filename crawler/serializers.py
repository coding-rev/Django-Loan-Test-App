from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

class LoanCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["country"]


class LoanSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["sector"]