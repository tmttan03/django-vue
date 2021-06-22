from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include

from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/users/', include('users.urls')),
    path('api/features/', include('features.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
