from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticateToQueryMiddlewareTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="matcha",
            password="password",
            email="matcha@latte.com",
        )

    def test_query_param_to_login(self):
        response = self.client.get(reverse("screenshot:index"), {"_user": "matcha"})

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "matcha")

    def test_query_param_to_login_with_invalid_user(self):
        response = self.client.get(reverse("screenshot:index"), {"_user": "anonymous"})

        self.assertEqual(response.status_code, 403)
