from django.contrib.auth.admin import UserAdmin

from main.admin import docs_screenshot_site
from .models import UserForScreenshot

docs_screenshot_site.register(UserForScreenshot, UserAdmin)
