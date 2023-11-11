from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(models.Manager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email_address, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email_address:
            raise ValueError(_("The Email must be set"))
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save()
        return user
