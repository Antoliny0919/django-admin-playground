from .admin import after_site, before_site, compare_site

MY_ADMINS = [after_site, before_site, compare_site]


def register(model, model_admin=None, **kwargs):
    for site in MY_ADMINS:
        site.register(model, model_admin, **kwargs)
