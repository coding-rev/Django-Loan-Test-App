# Python/django imports
from rest_framework import serializers

# Local apps imports
from .models.country_model import Country
from .models.loan_model import Loan
from .models.sector_model import Sector

""" Defined serializer for country model """


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


""" Defined serializer for sector model """


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


""" Defined serializer for loan model """


class LoanSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    country = CountrySerializer()

    class Meta:
        model = Loan
        fields = "__all__"
