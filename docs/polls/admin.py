from django.contrib import admin

from docs.admin import screenshot_site

from .models import (
    Choice,
    Question,
    QuestionAdmin07,
    QuestionAdmin08,
    QuestionAdmin10,
    QuestionAdmin11,
    QuestionAdmin12,
    QuestionAdmin13,
    QuestionAdmin14,
)


class QuestionAdmin07ModelAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]


class QuestionAdmin08ModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]


class ChoiceInlineAdmin10(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin10ModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInlineAdmin10]


class ChoiceInlineAdmin11(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin11ModelAdmin(admin.ModelAdmin):
    inlines = [ChoiceInlineAdmin11]


class QuestionAdmin12ModelAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]


class QuestionAdmin13ModelAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]


class ChoiceInlineAdmin14(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionAdmin14ModelAdmin(admin.ModelAdmin):
    inlines = [ChoiceInlineAdmin14]


screenshot_site.register(Choice)
screenshot_site.register(Question)
screenshot_site.register(QuestionAdmin07, QuestionAdmin07ModelAdmin)
screenshot_site.register(QuestionAdmin08, QuestionAdmin08ModelAdmin)
screenshot_site.register(QuestionAdmin10, QuestionAdmin10ModelAdmin)
screenshot_site.register(QuestionAdmin11, QuestionAdmin11ModelAdmin)
screenshot_site.register(QuestionAdmin12, QuestionAdmin12ModelAdmin)
screenshot_site.register(QuestionAdmin13, QuestionAdmin13ModelAdmin)
screenshot_site.register(QuestionAdmin14, QuestionAdmin14ModelAdmin)
