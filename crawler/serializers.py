from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

class LoanCountrySerializer(serializers.Serializer):
    country = serializers.CharField()


class LoanSectorSerializer(serializers.Serializer):
    sectors = serializers.CharField()