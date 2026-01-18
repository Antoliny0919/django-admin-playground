import os
from pathlib import Path

import pytest
from django.contrib.auth.models import User
from playwright.sync_api import expect, sync_playwright

expect.set_options(timeout=5_000)

AUTHENTICATION_STATE_FILE_PATH = Path("playwright/.auth/state.json")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(request, playwright):
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    is_headless = request.config.getoption("--headed")
    browser = playwright.chromium.launch(headless=not is_headless)
    yield browser
    browser.close()


@pytest.fixture
def user(db):
    return User.objects.create_superuser(
        username="super",
        email="super@admin.com",
        password="password",
    )


@pytest.fixture
def auth_storage_state(live_server, browser, user):
    # if AUTHENTICATION_STATE_FILE_PATH.exists():
    #     # Skip authentication if auth data already exists
    #     return None  # noqa: ERA001

    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{live_server.url}/before_admin/login/")
    page.fill("input[name='username']", user.username)
    page.fill("input[name='password']", "password")
    page.click("text=Log in")

    page.wait_for_load_state("networkidle")
    storage = context.storage_state(path=str(AUTHENTICATION_STATE_FILE_PATH))
    page.close()
    context.close()
    return storage


@pytest.fixture
def auth_page(browser, auth_storage_state, live_server):
    context = browser.new_context(storage_state=str(AUTHENTICATION_STATE_FILE_PATH))
    page = context.new_page()

    yield page

    page.close()
    context.close()
