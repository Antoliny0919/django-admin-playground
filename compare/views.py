from django.views.generic.base import TemplateView

from main.admin import compare_site


class BaseView(TemplateView):
    template_name = "compare/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_list"] = compare_site.get_app_list(self.request)
        return context


class IndexView(BaseView):
    template_name = "compare/index.html"


class LoginView(BaseView):
    template_name = "compare/login.html"


class PasswordChangeView(BaseView):
    template_name = "compare/password_change.html"


class PasswordChangeDoneView(BaseView):
    template_name = "compare/password_change_done.html"


class AppIndexView(BaseView):
    template_name = "compare/app_index.html"


class ChangeListView(BaseView):
    template_name = "compare/change_list.html"


class AddView(BaseView):
    template_name = "compare/add.html"


class ChangeView(BaseView):
    template_name = "compare/change.html"


class HistoryView(BaseView):
    template_name = "compare/history.html"


class DeleteView(BaseView):
    template_name = "compare/delete.html"
