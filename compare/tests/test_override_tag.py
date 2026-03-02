from pathlib import Path

from django.template import RequestContext, Template
from django.test import RequestFactory, TestCase, override_settings

BASE_DIR = Path(__file__).resolve().parent


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                BASE_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
                "builtins": [
                    "compare.templatetags.base",
                ],
            },
        },
    ],
)
class CustomLoaderTagTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    def render_template(self, string, request, context=None):
        context = context or {}
        context = RequestContext(request, context)
        return Template(string).render(context)

    def test_after_admin_include_tag_render(self):
        request = self.factory.get("/after_admin/some_path/")
        rendered = self.render_template(
            "{% include 'admin/test_template.html' %}",
            request,
        )
        self.assertEqual(rendered, "<h1>Hello World After Admin!</h1>\n")

    def test_before_admin_include_tag_render(self):
        request = self.factory.get("/before_admin/some_path/")
        rendered = self.render_template(
            "{% include 'admin/test_template.html' %}",
            request,
        )
        self.assertEqual(rendered, "<h1>Hello World Before Admin!</h1>\n")

    def test_before_admin_include_tag_unknown_template_render(self):
        request = self.factory.get("/before_admin/some_path/")
        rendered = self.render_template(
            "{% include 'admin/only_after.html' %}",
            request,
        )
        self.assertEqual(
            rendered,
            "<span>This template only exists in after_admin</span>\n",
        )

    def test_before_admin_inner_include_tag_render(self):
        request = self.factory.get("/before_admin/some_path/")
        rendered = self.render_template(
            "{% include 'admin/have_include.html' %}",
            request,
        )
        self.assertEqual(
            rendered,
            "<h1>Hello World Before Admin!</h1>\n\n<div>have include!</div>\n",
        )

    def test_after_admin_extends_tag_render(self):
        request = self.factory.get("/after_admin/some_path/")
        rendered = self.render_template(
            "{% extends 'admin/test_extends_tag.html' %}"
            "{% block some %}{{ block.super }}<span>render</span>{% endblock %}",
            request,
        )
        self.assertEqual(
            rendered,
            "<h1>Hello World After Admin!</h1><span>render</span>\n",
        )

    def test_before_admin_extends_tag_render(self):
        request = self.factory.get("/before_admin/some_path/")
        rendered = self.render_template(
            "{% extends 'admin/test_extends_tag.html' %}"
            "{% block some%}{{ block.super }}<span>render</span>{% endblock %}",
            request,
        )
        self.assertEqual(
            rendered,
            "<h1>Hello World Before Admin!</h1><span>render</span>"
            "\n<div>chicken!</div>\n",
        )

    def test_before_admin_extends_tag_chain_render(self):
        request = self.factory.get("/before_admin/some_path/")
        rendered = self.render_template(
            "{% extends 'admin/test_extends_chain.html' %}"
            "{% block some %}<h1>Hello Antoliny!</h1>{% block inner_some %}"
            "<div>I love chicken</div>{% endblock %}{% endblock %}"
            "{% block another %}{% endblock %}",
            request,
        )
        self.assertEqual(
            rendered,
            "<h1>Hello Antoliny!</h1><div>I love chicken</div>\n\n",
        )
