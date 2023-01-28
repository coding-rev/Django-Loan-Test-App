# Python/django imports
from rest_framework import serializers

# Local apps imports
from .models.country_model import Country
from .models.loan_model import Loan
from .models.sector_model import Sector
from .models.currency_model import Currency


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    country = CountrySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Loan
        fields = "__all__"
