import contextlib

from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.template import Library, TemplateDoesNotExist
from django.template.library import InclusionNode
from django.template.loader_tags import IncludeNode, construct_relative_path, do_include

register = Library()


class InclusionCompareAdminNode(InclusionAdminNode):
    def render(self, context):
        opts = context["opts"]
        app_label = opts.app_label.lower()
        object_name = opts.model_name
        site_template_prefix = context["site_template_prefix"]
        # Load template for this render call. (Setting self.filename isn't
        # thread-safe.)
        context.render_context[self] = context.template.engine.select_template(
            [
                f"{site_template_prefix}/{app_label}/{object_name}/{self.template_name}",
                f"{site_template_prefix}/{app_label}/{self.template_name}",
                f"{site_template_prefix}/{self.template_name}",
            ],
        )
        return InclusionNode.render(self, context)


class CustomIncludeNode(IncludeNode):
    def render(self, context):
        path = context.request.path
        if "before_admin" in path:
            original_name = self.template.resolve(context)
            new_name = original_name.replace("admin", "before_admin")
            original_key = (
                construct_relative_path(self.origin.template_name, original_name),
            )
            new_key = (construct_relative_path(self.origin.template_name, new_name),)
            cache = context.render_context.dicts[0].setdefault(self, {})
            # Pre-populate the cache with the modified template
            # before looking up the cache in IncludeNode render.
            if original_key not in cache:
                with contextlib.suppress(TemplateDoesNotExist):
                    cache[original_key] = context.template.engine.select_template(
                        new_key,
                    )
        return super().render(context)


@register.tag("include")
def custon_do_include(parser, token):
    node = do_include(parser, token)
    return CustomIncludeNode(
        node.template,
        extra_context=node.extra_context,
        isolated_context=node.isolated_context,
    )
