from django.contrib import admin
from django.core.exceptions import ValidationError

from main.utils import register

from .models import CustomWidgetInline
from .models import ErrorInline
from .models import FieldsetInline
from .models import HelpTextInline
from .models import Inline
from .models import LongInline
from .models import ManyToManyInline


class TabularInline(admin.TabularInline):
    model = Inline
    extra = 1
    verbose_name = "Tabular Inline"


class StackedInline(admin.StackedInline):
    model = Inline
    extra = 1
    verbose_name = "Stacked Inline"


class LinkTabularInline(admin.TabularInline):
    model = Inline
    extra = 1
    show_change_link = True
    verbose_name = "Link Tabular Inline"


class LinkStackedInline(admin.StackedInline):
    model = Inline
    extra = 1
    show_change_link = True
    verbose_name = "Link Stacked Inline"


class CollapseTabularInline(admin.TabularInline):
    model = Inline
    classes = ("collapse",)
    extra = 1
    verbose_name = "Collapse Tabular Inline"


class CollapseStackedInline(admin.StackedInline):
    model = Inline
    classes = ("collapse",)
    extra = 1
    verbose_name = "Collapse Stacked Inline"


class LongTabularInline(admin.TabularInline):
    model = LongInline
    verbose_name = "Long Tabular Inline"
    extra = 10


class LongStackedInline(admin.StackedInline):
    model = LongInline
    verbose_name = "Long Stacked Inline"
    extra = 10


class ReadonlyTabularInline(admin.TabularInline):
    model = LongInline
    verbose_name = "Readonly Tabular Inline"
    extra = 1
    readonly_fields = ("char", "text", "integer", "boolean", "email", "decimal")


class ReadonlyStackedInline(admin.TabularInline):
    model = LongInline
    verbose_name = "Readonly Stacked Inline"
    extra = 1
    readonly_fields = ("char", "text", "integer", "boolean", "email", "decimal")


class CustomFieldsetsTabularInline(admin.TabularInline):
    model = LongInline
    verbose_name = "Custom Fieldsets Tabular Inline"
    fieldsets = [
        (None, {"fields": ("text",)}),
        ("fieldset1", {"fields": ("char", "integer")}),
        (
            "fieldset2",
            {"fields": ("boolean", "email", "decimal"), "classes": ("collapse",)},
        ),
    ]
    extra = 1


class CustomFieldsetsStackedInline(admin.StackedInline):
    model = LongInline
    verbose_name = "Custom Fieldsets Stacked Inline"
    fieldsets = [
        (None, {"fields": ("text",)}),
        ("fieldset1", {"fields": ("char", "integer")}),
        (
            "fieldset2",
            {"fields": ("boolean", "email", "decimal"), "classes": ("collapse",)},
        ),
    ]
    extra = 1


class FieldsetTabularInline(admin.TabularInline):
    model = FieldsetInline
    verbose_name = "Fieldset Tabular Inline"
    extra = 1


class FieldsetStackedInline(admin.StackedInline):
    model = FieldsetInline
    verbose_name = "Fieldset Stacked Inline"
    extra = 1


class CustomWidgetTabularInline(admin.TabularInline):
    model = CustomWidgetInline
    verbose_name = "Custom Widget Tabular Inline"
    extra = 1


class CustomWidgetStackedInline(admin.StackedInline):
    model = CustomWidgetInline
    verbose_name = "Custom Widget Stacked Inline"
    extra = 1


class ManyToManyFieldTabularInline(admin.TabularInline):
    model = ManyToManyInline
    verbose_name = "ManyToMany Field Tabular Inline"
    extra = 1
    filter_vertical = ["m2m_2"]
    filter_horizontal = ["m2m_3"]


class ManyToManyFieldStackedInline(admin.StackedInline):
    model = ManyToManyInline
    verbose_name = "ManyToMany Field Stacked Inline"
    extra = 1
    filter_vertical = ["m2m_2"]
    filter_horizontal = ["m2m_3"]


class HelpTextTabularInline(admin.TabularInline):
    model = HelpTextInline
    verbose_name = "Help Text Tabular Inline"
    extra = 1


class HelpTextStackedInline(admin.StackedInline):
    model = HelpTextInline
    verbose_name = "Help Text Stacked Inline"
    extra = 1


class FormErrorTabularInline(admin.TabularInline):
    model = ErrorInline
    verbose_name = "Form Error Tabular Inline"
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class CustomFormSet(formset):
            def clean(self):
                raise ValidationError("Non Form Errors")

        return CustomFormSet


class FormErrorStackedInline(admin.StackedInline):
    model = ErrorInline
    verbose_name = "Form Error Stacked Inline"
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class CustomFormSet(formset):
            def clean(self):
                raise ValidationError("Non Form Errors")

        return CustomFormSet


register(
    Inline,
    inlines=[
        TabularInline,
        StackedInline,
        LinkTabularInline,
        LinkStackedInline,
        CollapseTabularInline,
        CollapseStackedInline,
    ],
)
register(
    LongInline,
    inlines=[
        ReadonlyTabularInline,
        ReadonlyStackedInline,
        CustomFieldsetsTabularInline,
        CustomFieldsetsStackedInline,
        LongTabularInline,
        LongStackedInline,
    ],
)
register(FieldsetInline, inlines=[FieldsetTabularInline, FieldsetStackedInline])
register(
    CustomWidgetInline,
    inlines=[CustomWidgetTabularInline, CustomWidgetStackedInline],
)
register(
    ManyToManyInline,
    inlines=[ManyToManyFieldTabularInline, ManyToManyFieldStackedInline],
)
register(HelpTextInline, inlines=[HelpTextTabularInline, HelpTextStackedInline])
register(ErrorInline, inlines=[FormErrorTabularInline, FormErrorStackedInline])
