from inspect import getfullargspec

from django.template.library import InclusionNode, parse_bits


class InclusionCompareAdminNode(InclusionNode):
    def __init__(self, parser, token, func, template_name, takes_context=True):
        self.template_name = template_name
        params, varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(
            func,
        )
        bits = token.split_contents()
        args, kwargs = parse_bits(
            parser,
            bits[1:],
            params,
            varargs,
            varkw,
            defaults,
            kwonly,
            kwonly_defaults,
            takes_context,
            bits[0],
        )
        super().__init__(func, takes_context, args, kwargs, filename=None)

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
        return super().render(context)
