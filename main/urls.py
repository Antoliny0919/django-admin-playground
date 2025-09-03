from django.contrib import admin
from django.urls import path, include

from .admin import before_site

urlpatterns = [
    path("before_admin/", before_site.urls),
    path("after_admin/", admin.site.urls),
    path("compare/", include("compare.urls")),
]
