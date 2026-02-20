from django import forms
from django.contrib import admin

from main.utils import register

from .models import (
    AllManyToMany,
    AutoComplete,
    Common,
    CustomWidget,
    FieldError,
    Fieldset,
    HelpText,
    HorizontalMultipleFields,
    Prepopulated,
    RawID,
    ReadOnly,
    VerboseName,
)


class BaseFormAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": (("char", "slug"), "choice")}),
        ("fieldset1", {"fields": ("text", "integer", "boolean")}),
        (
            "fieldset2",
            {"fields": (("file",), ("datetime",), ("fk",)), "classes": ("collapse",)},
        ),
    ]
    search_fields = ("char",)


class PrepopulatedAdmin(admin.ModelAdmin):
    fields = ("char", "slug")
    prepopulated_fields = {"slug": ("char",)}


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ("char", "choice", "slug", "integer", "datetime")


class VerboseNameForm(forms.ModelForm):
    model = VerboseName

    class Meta:
        labels = {
            "char": "char verbose name..",
            "text": "text verbose name..",
            "integer": "very " + "long " * 80 + "verbose name..",
            "fk": "fk verbose name..",
            "datetime": "datetime verbose name..",
        }


class VerboseNameAdmin(admin.ModelAdmin):
    form = VerboseNameForm


class HelpTextForm(forms.ModelForm):
    model = HelpText

    class Meta:
        help_texts = {
            "char": "char help text..",
            "slug": "very " + "long " * 80 + "help text..",
            "boolean": "boolean help text..",
            "datetime": "datetime help text..",
            "file": "file help text..",
        }


class HelpTextAdmin(admin.ModelAdmin):
    form = HelpTextForm


class FieldsetAdmin(admin.ModelAdmin):
    radio_fields = {"choice": admin.VERTICAL}
    filter_horizontal = ("m2m",)


class RawIDAdmin(admin.ModelAdmin):
    raw_id_fields = ("fk", "o2o", "m2m")


class AutocompleteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("fk", "m2m", "o2o")


class AllManyToManyAdmin(admin.ModelAdmin):
    filter_vertical = ("m2m_2",)
    filter_horizontal = ("m2m_3",)


class HorizontalMultipleFieldsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": (("char", "date", "datetime"),)}),
        ("fieldset1", {"fields": (("integer", "url", "m2m", "time"),)}),
    ]


register(Common, BaseFormAdmin)
register(Prepopulated, PrepopulatedAdmin)
register(ReadOnly, ReadOnlyAdmin)
register(VerboseName, VerboseNameAdmin)
register(HelpText, HelpTextAdmin)
register(CustomWidget)
register(Fieldset, FieldsetAdmin)
register(RawID, RawIDAdmin)
register(AutoComplete, AutocompleteAdmin)
register(AllManyToMany, AllManyToManyAdmin)
register(FieldError)
register(HorizontalMultipleFields, HorizontalMultipleFieldsAdmin)
