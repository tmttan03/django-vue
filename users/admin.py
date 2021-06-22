from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from users.models import User

admin.site.register(User)
admin.site.register(Permission)
