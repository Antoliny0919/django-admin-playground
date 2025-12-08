from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.template.library import InclusionNode


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
