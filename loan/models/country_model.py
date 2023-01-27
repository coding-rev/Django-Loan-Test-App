import uuid
from django.db import models
from setup.basemodel import TimeBaseModel


class Country(TimeBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name
