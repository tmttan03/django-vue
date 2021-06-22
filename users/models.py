import datetime
from time import gmtime, strftime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from rest_framework.authtoken.models import Token

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ Account User Information. """

    email = models.EmailField(max_length=500, unique=True)
    username = models.CharField(max_length=80, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    _image = _cover = None

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

    def get_token(self):
        """Generate a Valid User Token."""
        token, created = Token.objects.get_or_create(user=self)
        expiry_date = token.created + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_TIME)

        if not created and expiry_date < timezone.now():
            # delete token
            token.delete()
            # generate a new one
            token = Token.objects.create(user=self)

        return token

    def get_full_name(self):
        """Return User's Complete Name."""

        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name.title(),
                                  self.last_name.title())
        return self.email


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        User.get_token(instance)



