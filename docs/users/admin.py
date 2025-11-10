from django.contrib.auth.admin import UserAdmin

from main.utils import register
from .models import UserForScreenshot

register(UserForScreenshot, UserAdmin)
