from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.urls import path

from main.admin import CustomAdminSite


class ScreenshotAdminSite(CustomAdminSite):
    def get_urls(self):
        urlpatterns = super().get_urls()
        new_urlpatterns = [
            path("admin02_index/", self.index, name="admin02_index"),
            path("admin03_index/", self.index, name="admin03_index"),
        ]
        return new_urlpatterns + urlpatterns

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, None)
        if request.path.endswith("admin02_index/"):
            app_list = super().get_app_list(request, "auth")
        elif request.path.endswith("admin03_index/"):
            polls_list = super().get_app_list(request, "polls")
            # Keep only one Question model and remove the rest
            polls_list[0]["models"] = [
                model
                for model in polls_list[0]["models"]
                if model["object_name"] == "Question"
            ][:1]
            app_list = super().get_app_list(request, "auth") + polls_list
        return app_list

    def each_context(self, request):
        context = super().each_context(request)
        context["log_entries"] = LogEntry.objects.none()
        return context


screenshot_site = ScreenshotAdminSite(name="screenshot")
screenshot_site.register(User, UserAdmin)
screenshot_site.register(Group, GroupAdmin)
