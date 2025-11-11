from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


class AuthenticateToQueryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        username = request.GET.get("_user")
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                login(request, user)
            except User.DoesNotExist:
                raise PermissionDenied(f"Invalid user {username} supplied in query parameter")
        else:
            logout(request)

        return self.get_response(request)
