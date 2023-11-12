from django.db import models
from user.managers import UserManager
from django.contrib.postgres.fields import ArrayField


class Posting(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(to="user.Account", on_delete=models.CASCADE, null=False)
    product_name = models.CharField(max_length=50, unique=False)
    condition = models.EmailField(max_length=50, unique=False)
    price = models.FloatField(null=False)
    description = models.CharField(max_length=1000, unique=False)
    residential_hall = models.CharField(max_length=50, unique=False)
    categories = ArrayField(models.CharField(max_length=10, blank=False, null=False), size=8, blank=True)
