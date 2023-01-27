# Python/django imports
import uuid
from django.db import models

# Local apps imports
from setup.basemodel import TimeBaseModel
from .country_model import Country
from .sector_model import Sector


class Loan(TimeBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    signature_date = models.DateField()
    title = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="loan_country"
    )
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name="loan_sector"
    )
    signed_amount = models.CharField(max_length=100)

    def __str__(self):
        return self.title
