from django.contrib.auth.models import Group, User
from django.test import RequestFactory, TestCase, override_settings
from django.urls import path, reverse

from docs.admin import ScreenshotAdminSite
from docs.news.models import Article
from docs.polls.models import Choice, Question

test_site = ScreenshotAdminSite(name="test_screenshot")
test_site.register(User)
test_site.register(Group)
test_site.register(Question)
test_site.register(Choice)
test_site.register(Article)

urlpatterns = [
    path("test_screenshot_admin/", test_site.urls),
]


@override_settings(ROOT_URLCONF="docs.tests.test_site")
class ScreenshotAdminSiteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="tester",
            password="password",
            email="tester@world.com",
        )
        cls.factory = RequestFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_display_empty_recent_action_index_page(self):
        response = self.client.get(reverse("test_screenshot:index"))
        self.assertContains(
            response,
            (
                '<div class="module" id="recent-actions-module">'
                "<h2>Recent actions</h2><h3>My actions</h3><p>None available</p></div>"
            ),
            html=True,
        )

    def test_extra_index_page(self):
        response = self.client.get(reverse("test_screenshot:admin02_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Site administration</h1>")

        response = self.client.get(reverse("test_screenshot:admin03_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Site administration</h1>")

    def test_default_admin_index_app_list(self):
        request = self.factory.get(reverse("test_screenshot:index"))
        request.user = self.user

        app_list = test_site.get_app_list(request)
        self.assertEqual(len(app_list), 3)
        app_names = [app_data["name"] for app_data in app_list]
        self.assertEqual(
            app_names,
            ["Authentication and Authorization", "News", "Polls"],
        )

    def test_admin02_index_app_list(self):
        request = self.factory.get(reverse("test_screenshot:admin02_index"))
        request.user = self.user

        app_list = test_site.get_app_list(request)
        self.assertEqual(len(app_list), 1)
        self.assertEqual(app_list[0]["name"], "Authentication and Authorization")
        model_names = [model_data["name"] for model_data in app_list[0]["models"]]
        self.assertEqual(model_names, ["Groups", "Users"])

    def test_admin03_index_app_list(self):
        request = self.factory.get(reverse("test_screenshot:admin03_index"))
        request.user = self.user

        app_list = test_site.get_app_list(request)
        self.assertEqual(len(app_list), 2)
        app_names = [app_data["name"] for app_data in app_list]
        self.assertEqual(app_names, ["Authentication and Authorization", "Polls"])
        auth_app_model_names = [
            model_data["name"] for model_data in app_list[0]["models"]
        ]
        polls_app_model_names = [
            model_data["name"] for model_data in app_list[1]["models"]
        ]
        self.assertEqual(auth_app_model_names, ["Groups", "Users"])
        self.assertEqual(polls_app_model_names, ["Questions"])
