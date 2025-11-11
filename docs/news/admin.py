from django.contrib import admin, messages
from django.utils.translation import ngettext

from main.admin import docs_screenshot_site
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]
    ordering = ["title"]
    actions = ["make_published"]

    @admin.action(description="Mark selected stories as published")
    def make_published(self, request, queryset):
            updated = queryset.update(status="p")
            self.message_user(
                request,
                ngettext(
                    "%d story was successfully marked as published.",
                    "%d stories were successfully marked as published.",
                    updated,
                )
                % updated,
                messages.SUCCESS,
            )


docs_screenshot_site.register(Article, ArticleAdmin)
