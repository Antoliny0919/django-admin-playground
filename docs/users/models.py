from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class UserForScreenshot(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_for_screenshot_set",
        related_query_name="user_for_screenshot",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_for_screenshot_set",
        related_query_name="user_for_screenshot",
    )

    class Meta:
        verbose_name = "user"


class UserForScreenshotActions(UserForScreenshot):
    class Meta:
        proxy = True
        verbose_name = "user"
