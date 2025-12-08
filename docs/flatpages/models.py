from django.contrib.flatpages.models import FlatPage


class DocsFlatPage(FlatPage):
    class Meta:
        verbose_name = "flat page"
        verbose_name_plural = "flat pages"
