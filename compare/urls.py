from django.urls import path
from django.views.generic import TemplateView
from .views import IndexView


urlpatterns = [
    path("", TemplateView.as_view(template_name="compare/index.html")),
]
