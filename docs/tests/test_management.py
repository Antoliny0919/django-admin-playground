from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock


class MakeImageManagementCommandTestCase(TestCase):

    @patch('subprocess.run')
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_start_server_and_terminate(self, mock_sleep, mock_popen, mock_run):
        mock_server = MagicMock()
        mock_popen.return_value = mock_server

        call_command("makeimages")

        mock_popen.assert_called_once_with(
            ["python", "manage.py", "runserver", "8009"]
        )
        mock_sleep.assert_called_once_with(3)
        mock_server.terminate.assert_called_once()
