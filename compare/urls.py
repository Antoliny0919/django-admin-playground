from django.urls import path

from .views import (
    AddView,
    AppIndexView,
    ChangeListView,
    ChangeView,
    DeleteView,
    HistoryView,
    IndexView,
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
)

urlpatterns = [
    path("", IndexView.as_view()),
    path("login/", LoginView.as_view()),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view()),
    path("<str:app_name>/", AppIndexView.as_view()),
    path("<str:app_name>/<str:model_name>/", ChangeListView.as_view()),
    path("<str:app_name>/<str:model_name>/add/", AddView.as_view()),
    path("<str:app_name>/<str:model_name>/<int:pk>/change/", ChangeView.as_view()),
    path("<str:app_name>/<str:model_name>/<int:pk>/history/", HistoryView.as_view()),
    path("<str:app_name>/<str:model_name>/<int:pk>/delete/", DeleteView.as_view()),
]
