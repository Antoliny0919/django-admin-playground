from django.contrib import admin

from main.admin import docs_screenshot_site, for_admin03_screenshot_site

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


for_admin03_screenshot_site.register(Question)

docs_screenshot_site.register(Choice)
docs_screenshot_site.register(Question)
docs_screenshot_site.register(QuestionAdmin07, QuestionAdmin07ModelAdmin)
docs_screenshot_site.register(QuestionAdmin08, QuestionAdmin08ModelAdmin)
docs_screenshot_site.register(QuestionAdmin10, QuestionAdmin10ModelAdmin)
docs_screenshot_site.register(QuestionAdmin11, QuestionAdmin11ModelAdmin)
docs_screenshot_site.register(QuestionAdmin12, QuestionAdmin12ModelAdmin)
docs_screenshot_site.register(QuestionAdmin13, QuestionAdmin13ModelAdmin)
docs_screenshot_site.register(QuestionAdmin14, QuestionAdmin14ModelAdmin)
