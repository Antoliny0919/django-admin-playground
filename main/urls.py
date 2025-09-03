from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("after_admin/", admin.site.urls),
    path("compare/", include("compare.urls")),
]
