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

        call_command("makeimages", "admin01t")

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
        with self.assertRaisesMessage(
            CommandError, "apple is an image that cannot be generated"
        ):
            call_command("makeimages", "apple")
