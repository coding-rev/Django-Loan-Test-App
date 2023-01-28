import uuid
from django.db import models
from setup.basemodel import TimeBaseModel


class Currency(TimeBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="Euro", unique=True, max_length=50)
    symbol = models.CharField(unique=True, max_length=5)

    def __str__(self):
        return self.name
