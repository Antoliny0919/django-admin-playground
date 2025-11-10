import subprocess
import time

from django.core.management.base import BaseCommand, CommandError

PORT_NUMBER = "8009"

IMAGE_DATA = {
    "admin01t": {
        "path": "after_admin/login/",
        "selector": "#container",
        "output": "admin01t.png",
        "width": "394",
    }
}


class Command(BaseCommand):
    help = "Generates images used in the Django documentation."
    url = f"http://localhost:{PORT_NUMBER}"
    screen_width = 1200
    screen_height = 768

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the image to generate")

    def start_server(self):
        self.server = subprocess.Popen(
            ["python", "manage.py", "runserver", PORT_NUMBER]
        )
        time.sleep(3)  # wait for server to be ready

    def create_shot_scraper_command(self, path, selector, output, width, **kwargs):
        return [
            "shot-scraper",
            f"{self.url}/{path}",
            "-s",
            selector,
            "-o",
            output,
            "-w",
            width,
        ]

    def handle(self, *args, **options):
        name = options["name"]
        if name not in IMAGE_DATA.keys():
            raise CommandError(f"{name} is an image that cannot be generated")
        self.start_server()
        data = IMAGE_DATA[name]
        command = self.create_shot_scraper_command(
            data["path"],
            data["selector"],
            data["output"],
            data["width"]
        )
        subprocess.run(command)
        self.server.terminate()
