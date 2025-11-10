import subprocess
import time
from django.core.management.base import BaseCommand

PORT_NUMBER = "8009"


class Command(BaseCommand):
    help = "Generates images used in the Django documentation."
    url = f"http://localhost:{PORT_NUMBER}"

    def add_arguments(self, parser):
        pass

    def start_server(self):
        self.server = subprocess.Popen(
            ["python", "manage.py", "runserver", PORT_NUMBER]
        )
        time.sleep(3)  # wait for server to be ready

    def handle(self, *args, **options):
        self.start_server()
        subprocess.run([
            "shot-scraper", f"{self.url}/after_admin/"
        ])
        self.server.terminate()
