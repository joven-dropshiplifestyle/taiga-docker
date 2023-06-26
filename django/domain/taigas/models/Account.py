from django.db import models
from domain.commons.models.Base import BaseModel

import logging

logger = logging.getLogger(__name__)


class Account(BaseModel):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    project_id = models.IntegerField()
    project_name = models.CharField(max_length=100)
    project_slug = models.SlugField(max_length=100)
    project_description = models.CharField(max_length=1000)

    class Meta:
        ordering = ['id']

    def __str__(self):  # pragma: no cover
        return self.email
