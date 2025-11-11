from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.template.response import TemplateResponse
from django.urls import reverse


class CustomAdminSite(AdminSite):
    def __init__(self, name="admin", template_prefix="admin"):
        super().__init__(name)
        self.template_prefix = template_prefix

    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            response = view(request, *args, **kwargs)

            if isinstance(response, TemplateResponse):
                if isinstance(response.template_name, str):
                    response.template_name = self._modify_template_name(
                        response.template_name,
                    )
                elif isinstance(response.template_name, (list, tuple)):
                    response.template_name = [
                        self._modify_template_name(name)
                        for name in response.template_name
                    ]

            return response

        return super().admin_view(inner, cacheable)

    def each_context(self, request):
        context = super().each_context(request)
        context["site_template_prefix"] = self.template_prefix
        return context

    def _modify_template_name(self, template_name):
        """
        Replace template prefix to template_name.
        admin/index.html --> your_template_prefix/index.html
        """
        if template_name.startswith("admin/"):
            return template_name.replace("admin/", f"{self.template_prefix}/")
        return template_name


class CompareAdminSite(AdminSite):
    def _build_app_dict(self, request, label=None):
        """
        To provide the compare page in the sidebar,
        all URLs in app_dict are replaced with compare paths.
        """
        admin_path = reverse("admin:index").strip("/")
        app_dict = super()._build_app_dict(request, label)
        for app_data in app_dict.values():
            if app_data.get("app_url"):
                app_data["app_url"] = app_data["app_url"].replace(admin_path, "compare")
            for model_data in app_data["models"]:
                if model_data.get("admin_url"):
                    model_data["admin_url"] = model_data["admin_url"].replace(
                        admin_path,
                        "compare",
                    )
                if model_data.get("add_url"):
                    model_data["add_url"] = model_data["add_url"].replace(
                        admin_path,
                        "compare",
                    )
        return app_dict


class CustomFlatPageAdmin(FlatPageAdmin):
    # Customize the FlatPageAdmin as needed
    pass


before_site = CustomAdminSite(name="before_admin", template_prefix="before_admin")
after_site = CustomAdminSite()
# compare admin is not registered in the URL, only the object data is used.
compare_site = CompareAdminSite(name="compare")
for_admin02_screenshot_site = CustomAdminSite(name="admin01")
for_admin03_screenshot_site = CustomAdminSite(name="admin02")
docs_screenshot_site = CustomAdminSite(name="docs_screenshot")
for_admin02_screenshot_site.register(User, UserAdmin)
for_admin02_screenshot_site.register(Group, GroupAdmin)
for_admin03_screenshot_site.register(User, UserAdmin)
for_admin03_screenshot_site.register(Group, GroupAdmin)
docs_screenshot_site.register(User, UserAdmin)
docs_screenshot_site.register(Group, GroupAdmin)
before_site.register(User, UserAdmin)
before_site.register(Group, GroupAdmin)
before_site.register(FlatPage, FlatPageAdmin)
after_site.register(User, UserAdmin)
after_site.register(Group, GroupAdmin)
after_site.register(FlatPage, FlatPageAdmin)
compare_site.register(User, UserAdmin)
compare_site.register(Group, GroupAdmin)
compare_site.register(FlatPage, FlatPageAdmin)
