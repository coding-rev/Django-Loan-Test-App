import uuid
from django.db import models


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    signature_date = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    signed_amount = models.CharField(max_length=100)

    def __str__(self):
        return self.title
