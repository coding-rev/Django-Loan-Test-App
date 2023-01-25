import uuid
from django.db import models


class FinancedProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
