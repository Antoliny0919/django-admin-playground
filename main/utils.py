from django.contrib import admin
from .admin import before_site

MY_ADMINS = [admin.site, before_site]


def register(model, model_admin=None, inlines=[]):
    for site in MY_ADMINS:
        if inlines:
            site.register(model, inlines=inlines)
        elif model_admin:
            site.register(model, model_admin)
        else:
            site.register(model)
