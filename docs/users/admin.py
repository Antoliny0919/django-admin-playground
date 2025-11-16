from django.contrib.auth.admin import UserAdmin

from docs.admin import screenshot_site

from .models import UserForScreenshot, UserForScreenshotActions


class UserForScreenshotActionsModelAdmin(UserAdmin):
    list_filter = []


screenshot_site.register(UserForScreenshot, UserAdmin)
screenshot_site.register(
    UserForScreenshotActions,
    UserForScreenshotActionsModelAdmin,
)
