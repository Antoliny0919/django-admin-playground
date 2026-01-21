import pytest
from playwright.sync_api import expect


@pytest.mark.playwright
class TestCompareSidebarButtons:
    def get_frame_htmls(self, auth_page):
        before_frame = auth_page.locator("iframe#before").content_frame
        after_frame = auth_page.locator("iframe#after").content_frame

        return [before_frame.locator("html"), after_frame.locator("html")]

    def test_theme_change(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        htmls = self.get_frame_htmls(auth_page)
        htmls.append(auth_page.locator("html"))

        def htmls_have_attribute(htmls, value):
            for html in htmls:
                expect(html).to_have_attribute("data-theme", value)

        htmls_have_attribute(htmls, "auto")
        theme_change_button = auth_page.get_by_test_id("theme-toggle-button")

        theme_change_button.click()
        htmls_have_attribute(htmls, "light")

        theme_change_button.click()
        htmls_have_attribute(htmls, "dark")

        theme_change_button.click()
        htmls_have_attribute(htmls, "auto")

    def test_initial_theme_from_local_storage(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")
        auth_page.evaluate("() => localStorage.setItem('theme', 'dark')")
        auth_page.reload()

        before_html, after_html = self.get_frame_htmls(auth_page)
        expect(after_html).to_have_attribute("data-theme", "dark")
        expect(before_html).to_have_attribute("data-theme", "dark")

    def test_layout_direction_change(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        before_html, after_html = self.get_frame_htmls(auth_page)

        layout_direction_change_button = auth_page.locator(
            "button#layout-direction-toggle-button",
        )
        expect(after_html).to_have_attribute("dir", "ltr")
        expect(before_html).to_have_attribute("dir", "ltr")

        layout_direction_change_button.click()
        expect(after_html).to_have_attribute("dir", "rtl")
        expect(before_html).to_have_attribute("dir", "rtl")

        layout_direction_change_button.click()
        expect(after_html).to_have_attribute("dir", "ltr")
        expect(before_html).to_have_attribute("dir", "ltr")


@pytest.mark.playwright
class TestIframeNavbar:
    def get_browser_control_buttons(self, auth_page):
        return auth_page.locator("#before-browser-control button").all()

    def test_browser_control_buttons_initial_state(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        previous, next, refresh = self.get_browser_control_buttons(auth_page)

        expect(previous).to_be_disabled()
        expect(next).to_be_disabled()
        expect(refresh).to_be_enabled()

    def test_browser_control_buttons_change_state(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        previous, next, refresh = self.get_browser_control_buttons(auth_page)

        before_frame = auth_page.locator("iframe#before").content_frame
        before_frame.get_by_role("link", name="Changelist", exact=True).click()
        expect(previous).to_be_enabled()
        expect(next).to_be_disabled()

        before_frame.get_by_role("link", name="Paginations", exact=True).click()
        expect(previous).to_be_enabled()
        expect(next).to_be_disabled()

        previous.click()
        expect(previous).to_be_enabled()
        expect(next).to_be_enabled()

        refresh.click()
        expect(previous).to_be_enabled()
        expect(next).to_be_enabled()

        next.click()
        expect(previous).to_be_enabled()
        expect(next).to_be_disabled()

        previous.click()
        previous.click()
        expect(previous).to_be_disabled()
        expect(next).to_be_enabled()

    def test_browser_control_button_state_reset(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        previous, next, _ = self.get_browser_control_buttons(auth_page)

        before_frame = auth_page.locator("iframe#before").content_frame
        before_frame.get_by_role("link", name="Changelist", exact=True).click()
        expect(previous).to_be_enabled()
        expect(next).to_be_disabled()

        auth_page.reload()
        previous, next, _ = self.get_browser_control_buttons(auth_page)
        expect(previous).to_be_disabled()
        expect(next).to_be_disabled()

    def test_browser_url_value(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")

        browser_control_buttons = self.get_browser_control_buttons(auth_page)
        before_frame = auth_page.locator("iframe#before").content_frame
        previous = browser_control_buttons[0]

        url = auth_page.locator("#before-browser-toolbar input")
        expect(url).to_have_value(f"{live_server.url}/before_admin/")

        before_frame.get_by_role("link", name="Changelist", exact=True).click()
        expect(url).to_have_value(f"{live_server.url}/before_admin/changelist/")

        before_frame.get_by_role("link", name="Change password", exact=True).click()
        expect(url).to_have_value(f"{live_server.url}/before_admin/password_change/")

        previous.click()
        expect(url).to_have_value(f"{live_server.url}/before_admin/changelist/")
