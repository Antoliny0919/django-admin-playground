from django.contrib.flatpages.admin import FlatPageAdmin

from docs.admin import screenshot_site

from .models import DocsFlatPage

screenshot_site.register(DocsFlatPage, FlatPageAdmin)
