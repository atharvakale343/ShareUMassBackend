from django.db import models
from user.managers import UserManager


class Account(models.Model):
    email_address = models.EmailField(max_length=50, unique=True, primary_key=True)
    name = models.EmailField(max_length=50, unique=True, null=False)

    objects = UserManager()
