from django.db import models
from user.managers import UserManager


class Account(models.Model):
    email = models.EmailField(max_length=50, unique=True, primary_key=True)
    name = models.EmailField(max_length=50, unique=False, null=False)
    picture_url = models.URLField(null=False)

    objects = UserManager()


class SessionAccount(models.Model):
    account = models.ForeignKey(to="Account", on_delete=models.CASCADE, null=False)
    session_token = models.CharField(max_length=2000)
