from django.contrib import admin
from django.urls import include
from django.urls import path

from .admin import before_site

urlpatterns = [
    path("before_admin/", before_site.urls),
    path("after_admin/", admin.site.urls),
    path("compare/", include("compare.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
