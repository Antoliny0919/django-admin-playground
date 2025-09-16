from django.contrib import admin

from main.utils import register

from .models import Action
from .models import AllLink
from .models import ColumnSort
from .models import DateHierarchy
from .models import ForFk2Field
from .models import ForFkField
from .models import ForManyToManyField
from .models import ForOneToOneField
from .models import FullFilter
from .models import ListEditAble
from .models import ListFilter
from .models import Pagination
from .models import ReadOnly
from .models import Related
from .models import Search
from .models import VerboseName


class PaginationAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean")
    list_per_page = 2


class ListFilterAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "integer", "url", "date", "datetime", "fk")
    list_filter = ("id", "char", "boolean", "date", "fk")


class AllLinkAdmin(admin.ModelAdmin):
    list_display = (
        "char",
        "boolean",
        "integer",
        "file",
        "url",
        "date",
        "datetime",
        "fk",
    )
    list_display_links = (
        "char",
        "boolean",
        "integer",
        "file",
        "url",
        "date",
        "datetime",
        "fk",
    )


class ColumnSortAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "integer", "url", "date", "datetime", "fk")
    sortable_by = ("id", "boolean", "integer", "datetime")


class DateHierarchyAdmin(admin.ModelAdmin):
    list_display = ("char", "boolean", "integer", "datetime")
    date_hierarchy = "datetime"


class ListEditAbleAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "integer", "url", "date", "datetime", "fk")
    list_editable = ("char", "boolean", "integer", "url", "fk", "datetime")


class ReadOnlyAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "integer", "url")
    readonly_fields = ("char", "boolean", "url")


class SearchAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean")
    search_fields = ("id", "char")


class ActionAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    # actions_on_top = None  # noqa: ERA001
    # actions = None  # noqa: ERA001


class FullFilterAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "integer", "url", "date", "datetime", "fk")
    list_filter = ("id", "char", "boolean", "date", "fk")
    list_per_page = 2
    list_editable = ("char", "boolean", "url", "datetime")
    search_fields = ("id", "char")
    date_hierarchy = "datetime"


class RelatedChangeListAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "o2o__char", "fk__char", "fk__fk__char", "m2m__char")


class VerboseNameAdmin(admin.ModelAdmin):
    list_display = ("id", "char", "boolean", "time", "datetime")


register(Pagination, PaginationAdmin)
register(ListFilter, ListFilterAdmin)
register(AllLink, AllLinkAdmin)
register(ColumnSort, ColumnSortAdmin)
register(DateHierarchy, DateHierarchyAdmin)
register(ListEditAble, ListEditAbleAdmin)
register(ReadOnly, ReadOnlyAdmin)
register(Search, SearchAdmin)
register(Action, ActionAdmin)
register(FullFilter, FullFilterAdmin)
register(ForOneToOneField)
register(ForFkField)
register(ForFk2Field)
register(ForManyToManyField)
register(Related, RelatedChangeListAdmin)
register(VerboseName, VerboseNameAdmin)
