from django.contrib.auth.admin import UserAdmin

from main.admin import docs_screenshot_site

from .models import UserForScreenshot, UserForScreenshotActions


class UserForScreenshotActionsModelAdmin(UserAdmin):
    list_filter = []


docs_screenshot_site.register(UserForScreenshot, UserAdmin)
docs_screenshot_site.register(
    UserForScreenshotActions,
    UserForScreenshotActionsModelAdmin,
)
