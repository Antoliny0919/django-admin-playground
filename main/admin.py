from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group, Permission
from django.template.response import TemplateResponse


class CustomAdminSite(AdminSite):

    def __init__(self, name='admin', template_prefix='admin'):
        super().__init__(name)
        self.template_prefix = template_prefix

    def admin_view(self, view, cacheable=False):

        def inner(request, *args, **kwargs):
            response = view(request, *args, **kwargs)

            if isinstance(response, TemplateResponse):
                if isinstance(response.template_name, str):
                    response.template_name = self._modify_template_name(response.template_name)
                elif isinstance(response.template_name, (list, tuple)):
                    response.template_name = [
                        self._modify_template_name(name) for name in response.template_name
                    ]

            return response

        return super().admin_view(inner, cacheable)

    def _modify_template_name(self, template_name):
        """
        Replace template prefix to template_name.
        admin/index.html --> your_template_prefix/index.html
        """
        if template_name.startswith('admin/'):
            return template_name.replace('admin/', f'{self.template_prefix}/')
        return template_name


before_site = CustomAdminSite(template_prefix="before_admin")
before_site.register(User, UserAdmin)
before_site.register(Group, GroupAdmin)
before_site.register(Permission)
