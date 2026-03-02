from django.template import Library
from django.templatetags.static import StaticNode

register = Library()


class CustomStaticNode(StaticNode):
    def url(self, context):
        path = super().url(context)
        request_path = context.request.path
        if "before_admin" in request_path and path.startswith("/static/admin/"):
            path = path.replace("admin", "before_admin")
        return path


@register.tag("static")
def custom_do_static(parser, token):
    return CustomStaticNode.handle_token(parser, token)
