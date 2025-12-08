from django.contrib.admin.templatetags.admin_list import (
    admin_actions,
    date_hierarchy,
    pagination,
    paginator_number,
    result_list,
    search_form,
)
from django.template import Library
from django.template.loader import get_template

from .base import InclusionCompareAdminNode

# Make all tags used in admin use InclusionCompareAdminNode.
# InclusionCompareAdminNode determines which template to render
# based on the template_prefix applied to the site.

register = Library()


register.simple_tag(paginator_number, name="paginator_number")


@register.tag(name="pagination")
def pagination_tag(parser, token):
    return InclusionCompareAdminNode(
        "pagination",
        parser,
        token,
        func=pagination,
        template_name="pagination.html",
        takes_context=False,
    )


@register.tag(name="result_list")
def result_list_tag(parser, token):
    return InclusionCompareAdminNode(
        "result_list",
        parser,
        token,
        func=result_list,
        template_name="change_list_results.html",
        takes_context=False,
    )


@register.tag(name="date_hierarchy")
def date_hierarchy_tag(parser, token):
    return InclusionCompareAdminNode(
        "date_hierarchy",
        parser,
        token,
        func=date_hierarchy,
        template_name="date_hierarchy.html",
        takes_context=False,
    )


@register.tag(name="search_form")
def search_form_tag(parser, token):
    return InclusionCompareAdminNode(
        "search_form",
        parser,
        token,
        func=search_form,
        template_name="search_form.html",
        takes_context=False,
    )


@register.simple_tag
def admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    return tpl.render(
        {
            "title": spec.title,
            "choices": list(spec.choices(cl)),
            "spec": spec,
        },
    )


@register.tag(name="admin_actions")
def admin_actions_tag(parser, token):
    return InclusionCompareAdminNode(
        "admin_actions",
        parser,
        token,
        func=admin_actions,
        template_name="actions.html",
    )


@register.tag(name="change_list_object_tools")
def change_list_object_tools_tag(parser, token):
    """Display the row of change list object tools."""
    return InclusionCompareAdminNode(
        "change_list_object_tools",
        parser,
        token,
        func=lambda context: context,
        template_name="change_list_object_tools.html",
    )
