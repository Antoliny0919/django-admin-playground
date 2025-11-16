from django.urls import include, path

from docs.admin import screenshot_site

from .admin import (
    after_site,
    before_site,
)

urlpatterns = [
    path("before_admin/", before_site.urls),
    path("after_admin/", after_site.urls),
    path("compare/", include("compare.urls")),
    path("screenshot_admin/", screenshot_site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
