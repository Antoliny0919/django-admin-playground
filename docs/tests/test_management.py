import io
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandError, call_command
from django.core.management.base import OutputWrapper
from django.test import TestCase
from PIL import Image

from docs.management.commands.makeimages import Command


class MakeImageManagementCommandTestCase(TestCase):
    def setUp(self):
        self.command = Command()

        self.patch_sleep = patch("time.sleep")
        self.patch_popen = patch("subprocess.Popen")
        self.patch_run = patch("subprocess.run")
        self.patch_adjust = patch(
            "docs.management.commands.makeimages.Command.adjust_screenshot_size",
        )

        self.mock_sleep = self.patch_sleep.start()
        self.mock_popen = self.patch_popen.start()
        self.mock_run = self.patch_run.start()
        self.mock_adjust = self.patch_adjust.start()

        self.mock_server = MagicMock()
        self.mock_popen.return_value = self.mock_server

    def tearDown(self):
        self.patch_sleep.stop()
        self.patch_popen.stop()
        self.patch_run.stop()
        self.patch_adjust.stop()

    def test_start_server_and_terminate(self):
        call_command("makeimages", "admin01", "--noinput")

        self.mock_popen.assert_called_once_with(
            ["python", "manage.py", "runserver", "8009"],
        )
        self.mock_sleep.assert_called_once_with(3)
        self.mock_server.terminate.assert_called_once()

    def test_error_when_screenshot_not_specified(self):
        with self.assertRaisesMessage(
            CommandError,
            "Please provide at least one name or use --all option",
        ):
            call_command("makeimages")

    def test_invalid_name_argument(self):
        cases = [
            [["apple"], "apple"],
            [["admin01", "admin02", "admin889"], "admin889"],
        ]
        for case, invalid_name in cases:
            with (
                self.subTest(case=case),
                self.assertRaisesMessage(
                    CommandError,
                    (
                        f"{invalid_name} is not a valid screenshot name. "
                        "Use the -s or --screenshot-list option to view "
                        "the list of available screenshots"
                    ),
                ),
            ):
                call_command("makeimages", *case)

    def test_screenshot_file_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_output = Path(tmpdir) / "test_admin01.png"

            # Mock subprocess.run to create a dummy file
            def create_dummy_file(*args, **kwargs):
                # Extract output path from shot-scraper command
                command = args[0] if args else []
                if "--output" in command:
                    output_index = command.index("--output") + 1
                    output_path = command[output_index]
                    Path(output_path).touch()
                return MagicMock()

            self.mock_run.side_effect = create_dummy_file

            # Temporarily modify the config to use our temp directory
            with patch(
                "docs.management.commands.makeimages.SCREENSHOT_CONFIG",
                {
                    "test_admin": {
                        "path": "after_admin/login/",
                        "selector": "#container",
                        "output": temp_output,
                        "width": "1025",
                    },
                },
            ):
                call_command("makeimages", "test_admin", "--noinput")

                self.assertTrue(
                    temp_output.exists(),
                    f"Screenshot file {temp_output} was not created",
                )

                self.mock_popen.assert_called_once()
                self.mock_server.terminate.assert_called_once()

    @patch("pathlib.Path.mkdir")
    def test_screenshot_save_to_specific_directory(self, mock_mkdir):
        call_command(
            "makeimages",
            "admin01",
            "--output-dir",
            "hello/world/",
            "--noinput",
        )
        command_list = self.mock_run.call_args[0][0]
        output_index = command_list.index("--output") + 1
        self.assertEqual(
            command_list[output_index],
            str(Path("hello/world/").resolve() / "admin01t.png"),
        )

    def test_screenshot_save_to_default_directory(self):
        call_command("makeimages", "admin01", "--noinput")

        command_list = self.mock_run.call_args[0][0]
        output_index = command_list.index("--output") + 1
        self.assertEqual(
            command_list[output_index],
            str(Path("screenshots").resolve() / "admin01t.png"),
        )
        self.mock_server.terminate.assert_called_once()

    def test_output_directory_auto_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "nested/test/path"
            self.assertFalse(test_dir.exists())
            call_command("makeimages", "admin01", "--noinput", "--output-dir", test_dir)
            self.assertTrue(test_dir.exists())

    def test_generate_all_screenshot(self):
        with patch(
            "docs.management.commands.makeimages.SCREENSHOT_CONFIG",
            {
                "cheeze": {
                    "path": "after_admin/login/",
                    "output": "cheeze.png",
                },
                "hamburger": {
                    "path": "after_admin/login/",
                    "output": "hamburger.png",
                },
                "pizza": {
                    "path": "after_admin/login/",
                    "output": "pizza.png",
                },
            },
        ):
            call_command("makeimages", "--all", "--noinput")

            self.assertEqual(self.mock_run.call_count, 3)
            for call, output in zip(
                self.mock_run.call_args_list,
                ["cheeze.png", "hamburger.png", "pizza.png"],
                strict=True,
            ):
                command = call[0][0]
                output_idx = command.index("--output") + 1
                self.assertIn(output, command[output_idx])

    def test_screenshot_list_start_message_output(self):
        out = io.StringIO()
        call_command(
            "makeimages",
            "--screenshot-list",
            stdout=out,
        )
        out = out.getvalue()
        self.assertIn("This is a list of available image names for screenshots.", out)
        self.assertIn(
            "Check the names and pass the name of the image you want to "
            "capture as an argument.",
            out,
        )
        self.assertIn("Available screenshot names:", out)

    def test_screenshot_list_output(self):
        out = io.StringIO()
        with patch(
            "docs.management.commands.makeimages.DISPLAY_SCREENSHOT_LIST_DATA",
            {
                "admin_site": {
                    "link": "https://example.com/admin",
                    "names": ["admin01", "admin02"],
                },
                "user_management": {
                    "link": "https://example.com/users",
                    "names": ["user01"],
                },
            },
        ):
            call_command("makeimages", "--screenshot-list", stdout=out)
            output = out.getvalue()

            # Check group names are displayed
            self.assertIn("Admin Site", output)
            self.assertIn("User Management", output)

            # Check links are displayed
            self.assertIn("See: https://example.com/admin", output)
            self.assertIn("See: https://example.com/users", output)

            # Check screenshot names are displayed
            self.assertIn("admin01", output)
            self.assertIn("admin02", output)
            self.assertIn("user01", output)

    def test_screenshot_list_does_not_start_server(self):
        out = io.StringIO()
        with patch("subprocess.Popen") as mock_popen:
            call_command("makeimages", "--screenshot-list", stdout=out)

            # Server should not be started when just listing screenshots
            mock_popen.assert_not_called()

    def test_multiple_screenshots_at_once(self):
        with patch(
            "docs.management.commands.makeimages.SCREENSHOT_CONFIG",
            {
                "test_one": {
                    "path": "path/one/",
                    "output": "test_one.png",
                },
                "test_two": {
                    "path": "path/two/",
                    "output": "test_two.png",
                },
                "test_three": {
                    "path": "path/three/",
                    "output": "test_three.png",
                },
            },
        ):
            call_command("makeimages", "test_one", "test_two", "--noinput")

            # Verify subprocess.run was called twice (for two screenshots)
            self.assertEqual(self.mock_run.call_count, 2)

            self.mock_popen.assert_called_once()
            self.mock_server.terminate.assert_called_once()

    def test_all_option_with_output_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_dir = Path(tmpdir) / "custom_screenshots"

            with patch(
                "docs.management.commands.makeimages.SCREENSHOT_CONFIG",
                {
                    "shot_a": {
                        "path": "path/a/",
                        "output": "shot_a.png",
                    },
                    "shot_b": {
                        "path": "path/b/",
                        "output": "shot_b.png",
                    },
                },
            ):
                call_command(
                    "makeimages",
                    "--all",
                    "--output-dir",
                    custom_dir,
                    "--noinput",
                )
                # Verify all screenshots use the custom directory
                self.assertEqual(self.mock_run.call_count, 2)
                expected_dir = str(Path(custom_dir).resolve())
                for call in self.mock_run.call_args_list:
                    command = call[0][0]
                    output_idx = command.index("--output") + 1
                    self.assertTrue(command[output_idx].startswith(expected_dir))

    def test_retina_option_always_included(self):
        call_command("makeimages", "admin01", "--noinput")

        command_list = self.mock_run.call_args[0][0]
        self.assertIn("--retina", command_list)

    def test_direct_options_with_output_dir(self):
        call_command(
            "makeimages",
            "admin01",
            "--direct",
            "--output-dir",
            "aa/bb/cc",
            "--noinput",
        )
        command = self.mock_run.call_args[0][0]
        output_idx = command.index("--output") + 1
        # direct option takes precedence over the output_dir option
        self.assertIn("django/docs/intro/_images/admin01.png", command[output_idx])
        output_dir = Path("aa/bb/cc").resolve()
        self.assertFalse(output_dir.exists())

    @patch("builtins.input", return_value="")
    def test_generate_accept_confirm_with_enter(self, mock_input):
        out = io.StringIO()
        self.command.stdout = OutputWrapper(out)
        commands = [
            ["--output", "/aa/bb/cc/helloworld.png"],
            ["--output", "/factory/car/beautiful_car.png"],
            ["--output", "/cake/cheeze/newyork_cheeze_cake.png"],
        ]

        result = self.command.generate_accept_confirm(commands)
        output = out.getvalue()

        # input was called?
        mock_input.assert_called_once()

        self.assertTrue(result)
        self.assertIn("The following screenshots will be generated:", output)
        self.assertIn("/aa/bb/cc/helloworld.png", output)
        self.assertIn("/factory/car/beautiful_car.png", output)
        self.assertIn("/cake/cheeze/newyork_cheeze_cake.png", output)
        self.assertIn(
            "Press Enter to continue (or type anything else to cancel):",
            output,
        )

    @patch("builtins.input", return_value="no")
    def test_generate_accept_confirm_with_cancel(self, mock_input):
        out = io.StringIO()
        self.command.stdout = OutputWrapper(out)
        commands = [
            ["--output", "/test/screenshot.png"],
        ]

        result = self.command.generate_accept_confirm(commands)
        mock_input.assert_called_once()
        self.assertFalse(result)


class ScreenshotAdjustSizeTestCase(TestCase):
    def setUp(self):
        self.command = Command()

    def test_adjust_screenshot_size(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_image_path = Path(tmpdir) / "test_screenshot.png"
            test_img = Image.new("RGB", (800, 600), color="red")
            test_img.save(test_image_path)

            with patch(
                "docs.management.commands.makeimages.DJANGO_DOCS_SCREENSHOT_DATA",
                {"test_screenshot": {"width": 400}},
            ):
                self.command.adjust_screenshot_size("test_screenshot", test_image_path)

                resized_img = Image.open(test_image_path)
                self.assertEqual(resized_img.width, 400)
                # Height should be proportionally scaled (600 * 400/800 = 300)
                self.assertEqual(resized_img.height, 300)

    def test_adjust_screenshot_size_file_not_found(self):
        out = io.StringIO()
        self.command.stdout = OutputWrapper(out)

        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent_path = Path(tmpdir) / "does_not_exist.png"

            with patch(
                "docs.management.commands.makeimages.DJANGO_DOCS_SCREENSHOT_DATA",
                {"test_shot": {"width": 400}},
            ):
                # Should not raise an error, just print a warning
                self.command.adjust_screenshot_size("test_shot", non_existent_path)

                output = out.getvalue()
                self.assertIn("screenshot file not found", output)
                self.assertIn(str(non_existent_path), output)


class CreateShotScraperCommandTestCase(TestCase):
    def setUp(self):
        self.command = Command()

    @patch("pathlib.Path.mkdir")
    def test_create_shot_scraper_command(self, mock_mkdir):
        shot_scraper_command = self.command.create_shot_scraper_command(
            "admin01",
            "one/two/",
            Path("some_folder").resolve(),
            False,
            selector=".one div.two",
            output="numbers.png",
            height="400",
        )
        self.assertEqual(
            shot_scraper_command,
            [
                "shot-scraper",
                "http://localhost:8009/one/two/",
                "--retina",
                "--selector",
                ".one div.two",
                "--output",
                str(Path("some_folder").resolve() / "numbers.png"),
                "--height",
                "400",
            ],
        )

    @patch("pathlib.Path.mkdir")
    def test_create_shot_scraper_with_use_direct(self, mock_mkdir):
        shot_scraper_command = self.command.create_shot_scraper_command(
            "admin01",
            "one/two/",
            Path("some_folder").resolve(),
            True,
            selector=".one div.two",
            output="numbers.png",
            height="400",
        )
        output_idx = shot_scraper_command.index("--output")
        output_path = shot_scraper_command[output_idx + 1]
        self.assertIn("django/docs/intro/_images/admin01.png", output_path)

    @patch("pathlib.Path.mkdir")
    def test_unconfig_django_screenshot_path(self, mock_mkdir):
        with (
            patch(
                "docs.management.commands.makeimages.DJANGO_DOCS_SCREENSHOT_DATA",
                {"admin02": {"path": "some/django/path/admin02.png"}},
            ),
            self.assertRaisesMessage(
                ImproperlyConfigured,
                "Screenshot 'admin01' is not configured in "
                "DJANGO_DOCS_SCREENSHOT_DATA. "
                "Please add the mapping for 'admin01' in docs/config.py",
            ),
        ):
            self.command.create_shot_scraper_command(
                "admin01",
                "one/two/",
                Path("some_folder").resolve(),
                True,
                output="admin01.png",
            )
