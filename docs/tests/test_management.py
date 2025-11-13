import os
import io
import tempfile
from pathlib import Path

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandError
from django.core.management import call_command
from unittest.mock import patch, MagicMock

from docs.management.commands.makeimages import Command


class MakeImageManagementCommandTestCase(TestCase):

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_start_server_and_terminate(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages", "admin01")

        mock_popen.assert_called_once_with(
            ["python", "manage.py", "runserver", "8009"]
        )
        mock_sleep.assert_called_once_with(3)
        mock_server.terminate.assert_called_once()

    def test_create_shot_scraper_command(self):
        command = Command()
        shot_scraper_command = command.create_shot_scraper_command(
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
            ]
        )

    def test_create_shot_scraper_with_use_direct(self):
        command = Command()

        shot_scraper_command = command.create_shot_scraper_command(
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

    def test_unconfig_django_screenshot_path(self):
        command = Command()

        with patch('docs.management.commands.makeimages.DJANGO_DOCS_SCREENSHOT_PATH', {
            "admin02": "some/django/path/admin02.png"
        }):
            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "Screenshot 'admin01' is not configured in DJANGO_DOCS_SCREENSHOT_PATH. "
                "Please add the mapping for 'admin01' in docs/config.py"
            ):
                command.create_shot_scraper_command(
                    "admin01",
                    "one/two/",
                    Path("some_folder").resolve(),
                    True,
                    output="admin01.png",
                )

    def test_error_when_screenshot_not_specified(self):
        with self.assertRaisesMessage(
            CommandError, "Please provide at least one name or use --all option"
        ):
            call_command("makeimages")

    def test_invalid_name_argument(self):
        cases = [
            [["apple"], "apple"],
            [["admin01", "admin02", "admin889"], "admin889"],
        ]
        for case, invalid_name in cases:
            with self.subTest(case=case):
                with self.assertRaisesMessage(
                    CommandError, (
                        f"{invalid_name} is not a valid screenshot name"
                        "Use the -s or --screenshot-list option to view "
                        "the list of available screenshots"
                    )
                ):
                    call_command("makeimages", *case)

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_screenshot_file_creation(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        # Create a temporary directory for test screenshots
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_output = os.path.join(tmpdir, "test_admin01.png")

            # Mock subprocess.run to create a dummy file
            def create_dummy_file(*args, **kwargs):
                # Extract output path from shot-scraper command
                command = args[0] if args else []
                if "--output" in command:
                    output_index = command.index("--output") + 1
                    output_path = command[output_index]
                    Path(output_path).touch()
                return MagicMock()

            mock_run.side_effect = create_dummy_file

            # Temporarily modify the config to use our temp directory
            with patch('docs.management.commands.makeimages.SCREENSHOT_CONFIG', {
                'test_admin': {
                    'path': 'after_admin/login/',
                    'selector': '#container',
                    'output': temp_output,
                    'width': '1025',
                }
            }):
                call_command("makeimages", "test_admin")

                self.assertTrue(
                    os.path.exists(temp_output),
                    f"Screenshot file {temp_output} was not created"
                )

                mock_popen.assert_called_once()
                mock_server.terminate.assert_called_once()

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_screenshot_save_to_specific_directory(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages", "admin01", "--output-dir", "hello/world/")

        command_list = mock_run.call_args[0][0]
        output_index = command_list.index("--output") + 1
        self.assertEqual(
            command_list[output_index],
            str(Path("hello/world/").resolve() / "admin01t.png"),
        )

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_screenshot_save_to_default_directory(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages", "admin01")

        command_list = mock_run.call_args[0][0]
        output_index = command_list.index("--output") + 1
        self.assertEqual(
            command_list[output_index],
            str(Path("screenshots").resolve() / "admin01t.png"),
        )
        mock_server.terminate.assert_called_once()

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_output_directory_creation(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "nested/test/path")

            call_command("makeimages", "admin01", "--output-dir", test_dir)

            self.assertTrue(
                os.path.exists(test_dir),
                f"Directory {test_dir} was not created"
            )

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_generate_all_screenshot(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        with patch('docs.management.commands.makeimages.SCREENSHOT_CONFIG', {
            'cheeze': {
                'path': 'after_admin/login/',
                'output': 'cheeze.png',
            },
            'hamburger': {
                'path': 'after_admin/login/',
                'output': 'hamburger.png',
            },
            'pizza': {
                'path': 'after_admin/login/',
                'output': 'pizza.png',
            }
        }):
            call_command("makeimages", "--all")

            self.assertEqual(mock_run.call_count, 3)
            for call, output in zip(
                mock_run.call_args_list, ["cheeze.png", "hamburger.png", "pizza.png"]
            ):
                command = call[0][0]
                output_idx = command.index('--output') + 1
                self.assertIn(output, command[output_idx])

    def test_screenshot_list_start_message_output(self):
        out = io.StringIO()
        call_command(
            "makeimages", "--screenshot-list", stdout=out,
        )
        out = out.getvalue()
        self.assertIn("This is a list of available image names for screenshots.", out)
        self.assertIn(
            "Check the names and pass the name of the image you want to capture as an argument.",
            out,
        )
        self.assertIn("Available screenshot names:", out)

    def test_screenshot_list_output(self):
        out = io.StringIO()
        with patch('docs.management.commands.makeimages.DISPLAY_SCREENSHOT_LIST_DATA', {
            'admin_site': {
                'link': 'https://example.com/admin',
                'names': ['admin01', 'admin02']
            },
            'user_management': {
                'link': 'https://example.com/users',
                'names': ['user01']
            }
        }):
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
        with patch('subprocess.Popen') as mock_popen:
            call_command("makeimages", "--screenshot-list", stdout=out)

            # Server should not be started when just listing screenshots
            mock_popen.assert_not_called()

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_multiple_screenshots_at_once(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        with patch('docs.management.commands.makeimages.SCREENSHOT_CONFIG', {
            'test_one': {
                'path': 'path/one/',
                'output': 'test_one.png',
            },
            'test_two': {
                'path': 'path/two/',
                'output': 'test_two.png',
            },
            'test_three': {
                'path': 'path/three/',
                'output': 'test_three.png',
            }
        }):
            call_command("makeimages", "test_one", "test_two")

            # Verify subprocess.run was called twice (for two screenshots)
            self.assertEqual(mock_run.call_count, 2)

            mock_popen.assert_called_once()
            mock_server.terminate.assert_called_once()

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_all_option_with_output_dir(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        with tempfile.TemporaryDirectory() as tmpdir:
            custom_dir = os.path.join(tmpdir, "custom_screenshots")

            with patch('docs.management.commands.makeimages.SCREENSHOT_CONFIG', {
                'shot_a': {
                    'path': 'path/a/',
                    'output': 'shot_a.png',
                },
                'shot_b': {
                    'path': 'path/b/',
                    'output': 'shot_b.png',
                }
            }):
                call_command("makeimages", "--all", "--output-dir", custom_dir)

                self.assertTrue(os.path.exists(custom_dir))

                # Verify all screenshots use the custom directory
                self.assertEqual(mock_run.call_count, 2)
                expected_dir = str(Path(custom_dir).resolve())
                for call in mock_run.call_args_list:
                    command = call[0][0]
                    output_idx = command.index('--output') + 1
                    self.assertTrue(command[output_idx].startswith(expected_dir))

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_retina_option_always_included(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages", "admin01")

        command_list = mock_run.call_args[0][0]
        self.assertIn("--retina", command_list)
        mock_server.terminate.assert_called_once()

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_direct_options_with_output_dir(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages", "admin01", "--direct", "--output-dir", "aa/bb/cc")
        command = mock_run.call_args[0][0]
        output_idx = command.index('--output') + 1
        # direct option takes precedence over the output_dir option
        self.assertIn("django/docs/intro/_images/admin01.png", command[output_idx])
