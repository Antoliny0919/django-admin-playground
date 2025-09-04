from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="compare/index.html")),
    path("login/", TemplateView.as_view(template_name="compare/login.html")),
    path("password_change/", TemplateView.as_view(template_name="compare/password_change.html")),
    path("password_change/done/", TemplateView.as_view(template_name="compare/password_change_done.html")),
    path("<str:app_name>/", TemplateView.as_view(template_name="compare/app_index.html")),

    path("<str:app_name>/<str:model_name>/", TemplateView.as_view(template_name="compare/changelist.html")),
    path("<str:app_name>/<str:model_name>/add/", TemplateView.as_view(template_name="compare/add.html")),
    path("<str:app_name>/<str:model_name>/<int:pk>/change/", TemplateView.as_view(template_name="compare/change.html")),
    path("<str:app_name>/<str:model_name>/<int:pk>/history/", TemplateView.as_view(template_name="compare/history.html")),
    path("<str:app_name>/<str:model_name>/<int:pk>/delete/", TemplateView.as_view(template_name="compare/delete.html")),
]
