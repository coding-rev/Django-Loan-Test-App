# Python/django imports
from django.contrib import admin

# Local apps imports
from .models.country_model import Country
from .models.loan_model import Loan
from .models.sector_model import Sector
from .models.currency_model import Currency

# Register app to admin dashboard
admin.site.register(Country)
admin.site.register(Loan)
admin.site.register(Sector)
admin.site.register(Currency)
