from django.apps import AppConfig


class DocsFlatPagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "docs.flatpages"
    label = "docs_flatpages"
    verbose_name = "flatpages"
