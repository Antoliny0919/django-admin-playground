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

        before_html, after_html = self.get_frame_htmls(auth_page)

        expect(before_html).to_have_attribute("data-theme", "auto")
        expect(after_html).to_have_attribute("data-theme", "auto")
        theme_change_button = auth_page.get_by_test_id("theme-toggle-button")

        theme_change_button.click()
        expect(before_html).to_have_attribute("data-theme", "light")
        expect(after_html).to_have_attribute("data-theme", "light")

        theme_change_button.click()
        expect(before_html).to_have_attribute("data-theme", "dark")
        expect(after_html).to_have_attribute("data-theme", "dark")

        theme_change_button.click()
        expect(before_html).to_have_attribute("data-theme", "auto")
        expect(after_html).to_have_attribute("data-theme", "auto")

    def test_initial_theme_from_local_storage(self, auth_page, live_server):
        auth_page.goto(f"{live_server.url}/compare")
        auth_page.evaluate("() => localStorage.setItem('theme', 'dark')")
        auth_page.reload()

        before_html, after_html = self.get_frame_htmls(auth_page)
        expect(after_html).to_have_attribute("data-theme", "dark")
        expect(before_html).to_have_attribute("data-theme", "dark")
