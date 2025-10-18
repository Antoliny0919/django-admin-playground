from django.urls import include, path

from .admin import after_site, before_site

urlpatterns = [
    path("before_admin/", before_site.urls),
    path("after_admin/", after_site.urls),
    path("compare/", include("compare.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
