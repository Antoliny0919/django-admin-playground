from django.urls import include, path

from .admin import (
    after_site,
    before_site,
    docs_screenshot_site,
    for_admin02_screenshot_site,
    for_admin03_screenshot_site,
)

urlpatterns = [
    path("before_admin/", before_site.urls),
    path("after_admin/", after_site.urls),
    path("compare/", include("compare.urls")),
    path("admin02/", for_admin02_screenshot_site.urls),
    path("admin03/", for_admin03_screenshot_site.urls),
    path("docs_screenshot/", docs_screenshot_site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
