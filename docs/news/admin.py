from django.contrib import admin, messages
from django.utils.translation import ngettext

from docs.admin import screenshot_site

from .models import Article, NewsPaper, RawIDFields


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


class RawIDFieldsAdmin(admin.ModelAdmin):
    raw_id_fields = ["newspaper"]


screenshot_site.register(Article, ArticleAdmin)
screenshot_site.register(NewsPaper)
screenshot_site.register(RawIDFields, RawIDFieldsAdmin)
