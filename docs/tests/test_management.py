import os
import tempfile
from pathlib import Path

from django.test import TestCase
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
            "one/two/",
            selector=".one div.two",
            output="numbers.png",
            height="400",
        )
        self.assertEqual(
            shot_scraper_command,
            [
                "shot-scraper",
                "http://localhost:8009/one/two/",
                "--selector",
                ".one div.two",
                "--output",
                "numbers.png",
                "--height",
                "400",
            ]
        )

    def test_invalid_name_argument(self):
        cases = [
            ["apple"],
            ["admin01", "admin02", "admin889"],
        ]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaisesMessage(
                    CommandError, "Invalid name"
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
