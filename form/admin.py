from django import forms
from django.contrib import admin
from .models import (
    Common,
    Prepopulated,
    ReadOnly,
    VerboseName,
    HelpText,
    CustomWidget,
    Fieldset,
    RawID,
    AutoComplete,
    AllMtM,
    FieldError,
)

from main.utility import register


class BaseFormAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": (("char", "slug",), "choice")}),
        ("fieldset1", {"fields": ("text", "integer", "boolean")}),
        ("fieldset2", {"fields": (("file",), ("datetime",), ("fk",)), "classes": ("collapse",)}),
    ]
    search_fields = ("char",)


class PrepopulatedAdmin(admin.ModelAdmin):
    fields = ("char", "slug",)
    prepopulated_fields = {"slug": ("char",)}


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ("char", "choice", "slug", "integer", "datetime",)


class VerboseNameForm(forms.ModelForm):
    model = VerboseName

    class Meta:
        labels = {
            "char": "char verbose name..",
            "text": "text verbose name..",
            "integer": "integer verbose name..",
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
            "slug": "slug help text..",
            "boolean": "boolean help text..",
            "datetime": "datetime help text..",
            "file": "file help text..",
        }


class HelpTextAdmin(admin.ModelAdmin):
    form = HelpTextForm


class FieldsetAdmin(admin.ModelAdmin):
    radio_fields = {"choice": admin.VERTICAL}
    filter_horizontal = ("mtm",)


class RawIDAdmin(admin.ModelAdmin):
    raw_id_fields = ("fk", "oto", "mtm",)


class AutocompleteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("fk", "mtm", "oto")


class AllMtMAdmin(admin.ModelAdmin):
    filter_vertical = ("mtm2",)
    filter_horizontal = ("mtm3",)


register(Common, BaseFormAdmin)
register(Prepopulated, PrepopulatedAdmin)
register(ReadOnly, ReadOnlyAdmin)
register(VerboseName, VerboseNameAdmin)
register(HelpText, HelpTextAdmin)
register(CustomWidget)
register(Fieldset, FieldsetAdmin)
register(RawID, RawIDAdmin)
register(AutoComplete, AutocompleteAdmin)
register(AllMtM, AllMtMAdmin)
register(FieldError)
