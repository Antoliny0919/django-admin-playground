from django.contrib.auth import get_user_model, login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


class AuthenticateToQueryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        username = request.GET.get("_user")
        if username:
            user_model = get_user_model()
            try:
                user = user_model.objects.get(username=username)
                login(request, user)
            except user_model.DoesNotExist as err:
                msg = f"Invalid user {username} supplied in query parameter"
                raise PermissionDenied(msg) from err

        return self.get_response(request)
