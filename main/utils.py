from django.contrib import admin
from .admin import before_site

MY_ADMINS = [admin.site, before_site]


def register(model, model_admin=None, **kwargs):
    for site in MY_ADMINS:
        site.register(model, model_admin, **kwargs)
