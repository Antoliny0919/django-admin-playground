import subprocess
import time

from django.core.management.base import BaseCommand, CommandError

PORT_NUMBER = "8009"

IMAGE_DATA = {
    "admin01t": {
        "path": "after_admin/login/",
        "selector": "#container",
        "output": "admin01t.png",
        "width": "1025",
    },
    "admin02": {
        "path": "admin02/?_user=admin",
        "output": "admin02.png",
        "width": "1025",
        "height": "280",
    }
}


class Command(BaseCommand):
    help = "Generates images used in the Django documentation."
    url = f"http://localhost:{PORT_NUMBER}"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the image to generate")

    def start_server(self):
        self.server = subprocess.Popen(
            ["python", "manage.py", "runserver", PORT_NUMBER]
        )
        time.sleep(3)  # wait for server to be ready

    def create_shot_scraper_command(self, path, **options):
        command = ["shot-scraper", f"{self.url}/{path}"]
        for option in options:
            command.append(f"--{option}")
            command.append(options[option])
        return command

    def handle(self, *args, **options):
        name = options["name"]
        if name not in IMAGE_DATA.keys():
            raise CommandError(f"{name} is an image that cannot be generated")
        self.start_server()
        data = IMAGE_DATA[name]
        path = data.pop("path")
        command = self.create_shot_scraper_command(path, **data)
        subprocess.run(command)
        self.server.terminate()
