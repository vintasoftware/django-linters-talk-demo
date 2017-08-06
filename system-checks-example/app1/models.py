from django.db import models
from django.contrib.postgres.fields import ArrayField


class Post(models.Model):
    tags = ArrayField(
        models.CharField(max_length=200),
        default=[])
