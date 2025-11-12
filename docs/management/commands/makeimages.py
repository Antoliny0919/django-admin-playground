import subprocess
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from docs.config import SCREENSHOT_CONFIG

PORT_NUMBER = "8009"


class Command(BaseCommand):
    help = "Generates images used in the Django documentation."
    url = f"http://localhost:{PORT_NUMBER}"

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            nargs='+',
            help="Names of the image to generate"
        )
        parser.add_argument(
            "-d",
            "--output-dir",
            default="screenshots",
            help="Specifies the folder where screenshots will be saved",
        )

    def start_server(self):
        self.server = subprocess.Popen(
            ["python", "manage.py", "runserver", PORT_NUMBER]
        )
        time.sleep(3)  # wait for server to be ready

    def create_shot_scraper_command(self, path, output_dir, **options):
        command = ["shot-scraper", f"{self.url}/{path}", "--retina"]
        for option in options:
            value = options[option]
            if option == "output":
                value = str(output_dir / options[option])
            command.append(f"--{option}")
            command.append(value)
        return command

    def get_output_directory(self, output_dir):
        # Convert to absolute path and create directory if it doesn't exist
        output_dir_path = Path(output_dir).resolve()
        output_dir_path.mkdir(parents=True, exist_ok=True)
        return output_dir_path

    def handle(self, *args, **options):
        names = options["name"]
        if any(name not in SCREENSHOT_CONFIG.keys() for name in names):
            raise CommandError("Invalid name")
        self.start_server()
        output_dir = self.get_output_directory(options["output_dir"])
        for name in names:
            data = SCREENSHOT_CONFIG[name].copy()
            path = data.pop("path")
            command = self.create_shot_scraper_command(path, output_dir, **data)
            subprocess.run(command)
        self.server.terminate()
