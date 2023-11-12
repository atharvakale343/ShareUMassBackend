from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(models.Manager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, name, picture_url):
        """
        Create and save a User with the given email and password.
        """

        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, name=name, picture_url=picture_url)
        user.save()
        return user
