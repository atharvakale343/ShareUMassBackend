from django.db import models
from user.managers import UserManager


class Posting(models.Model):
    email = models.EmailField(max_length=50, unique=True, primary_key=True)
    name = models.EmailField(max_length=50, unique=True, null=False)
    picture_url = models.URLField(null=False)
