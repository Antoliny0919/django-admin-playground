import subprocess
import time
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style
from PIL import Image

from docs.config import (
    DISPLAY_SCREENSHOT_LIST_DATA,
    DJANGO_DOCS_SCREENSHOT_DATA,
    SCREENSHOT_CONFIG,
)

PORT_NUMBER = "8009"
style = color_style()


class Command(BaseCommand):
    help = "Generates images used in the Django documentation."
    url = f"http://localhost:{PORT_NUMBER}"

    def add_arguments(self, parser):
        parser.add_argument("name", nargs="*", help="Names of the image to generate")
        parser.add_argument(
            "-d",
            "--output-dir",
            default="screenshots",
            help="Specifies the folder where screenshots will be saved",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Generates all screenshots",
        )
        parser.add_argument(
            "-s",
            "--screenshot-list",
            action="store_true",
            help="display a list of available screenshots",
        )
        parser.add_argument(
            "--direct",
            action="store_true",
            help="Save screenshots directly to Django docs folder",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help=(
                "Instructs not to prompt for any confirmation input "
                "when generating screenshots"
            ),
        )

    def handle(self, *args, **options):  # noqa: C901
        names = options["name"]
        use_all = options["all"]
        show_screenshot_list = options["screenshot_list"]
        use_direct = options["direct"]
        output_dir = options["output_dir"]
        interactive = options["interactive"]
        if show_screenshot_list:
            self.stdout.write(self.get_screenshot_list() + "\n")
            return
        if not use_all and not names:
            raise CommandError("Please provide at least one name or use --all option")

        if not use_all:
            for name in names:
                if name not in SCREENSHOT_CONFIG:
                    msg = (
                        f"{name} is not a valid screenshot name. "
                        "Use the -s or --screenshot-list option to view "
                        "the list of available screenshots"
                    )
                    raise CommandError(msg)

        commands = []
        if use_all:
            names = SCREENSHOT_CONFIG.keys()
        for name in names:
            data = SCREENSHOT_CONFIG[name].copy()
            path = data.pop("path")
            command = self.create_shot_scraper_command(
                name,
                path,
                output_dir,
                use_direct,
                **data,
            )
            commands.append(command)
        accept = True
        if interactive:
            accept = self.generate_accept_confirm(commands)
        if accept:
            self.start_server()
            for command in commands:
                subprocess.run(command, check=False)
            self.server.terminate()
            # Resize the generated screenshot to the desired dimension
            for name, command in zip(names, commands):
                output_idx = command.index("--output")
                screenshot_path = command[output_idx + 1]
                self.adjust_screenshot_size(name, screenshot_path)
        else:
            self.stdout.write(style.WARNING("Screenshot generation cancelled"))

    def start_server(self):
        self.server = subprocess.Popen(
            ["python", "manage.py", "runserver", PORT_NUMBER],
        )
        time.sleep(3)  # wait for server to be ready

    def get_screenshot_save_path(self, name, output_dir, use_direct, value):
        if use_direct:
            if not hasattr(settings, "DJANGO_DIR"):
                raise ImproperlyConfigured(
                    "DJANGO_DIR setting is required when using --direct option. "
                    "Please add DJANGO_DIR to settings.py",
                )
            if name not in DJANGO_DOCS_SCREENSHOT_DATA:
                msg = (
                    f"Screenshot '{name}' is not configured in "
                    f"DJANGO_DOCS_SCREENSHOT_DATA. "
                    f"Please add the mapping for '{name}' in docs/config.py"
                )
                raise ImproperlyConfigured(msg)
            return str(settings.DJANGO_DIR / DJANGO_DOCS_SCREENSHOT_DATA[name]["path"])
        return str(self.get_output_directory(output_dir) / value)

    def create_shot_scraper_command(
        self,
        name,
        path,
        output_dir,
        use_direct,
        **options,
    ):
        command = ["shot-scraper", f"{self.url}/{path}", "--retina"]
        for option, option_value in options.items():
            final_value = option_value
            if option == "output":
                final_value = self.get_screenshot_save_path(
                    name,
                    output_dir,
                    use_direct,
                    option_value,
                )
            command.append(f"--{option}")
            command.append(final_value)
        return command

    def get_output_directory(self, output_dir):
        # Convert to absolute path and create directory if it doesn't exist
        output_dir_path = Path(output_dir).resolve()
        output_dir_path.mkdir(parents=True, exist_ok=True)
        return output_dir_path

    def generate_accept_confirm(self, commands):
        message = [
            style.NOTICE("The following screenshots will be generated:"),
            "",
        ]
        for command in commands:
            output_idx = command.index("--output")
            output_path = command[output_idx + 1]
            message.append(f"  • {output_path}")
        message.append("")
        message.append("Press Enter to continue (or type anything else to cancel): ")
        self.stdout.write("\n".join(message), ending="")
        accept = input()
        return accept == ""

    def get_screenshot_list(self):
        """
        Returns the message to be displayed for the screenshot list option.
        """
        usage = [
            "This is a list of available image names for screenshots.",
            "Check the names and pass the name of the image you want to "
            "capture as an argument.",
            "",
            "Available screenshot names:",
        ]
        for group in DISPLAY_SCREENSHOT_LIST_DATA:
            usage.append("")
            # Format group key for display (e.g., "admin_site" -> "Admin Site")
            group_text = group.replace("_", " ").title()
            link = DISPLAY_SCREENSHOT_LIST_DATA[group]["link"]
            usage.append(style.NOTICE(f"[{group_text}]"))
            usage.append(f"See: {link}")
            usage.extend(
                f"    {name}" for name in DISPLAY_SCREENSHOT_LIST_DATA[group]["names"]
            )

        return "\n".join(usage)

    def adjust_screenshot_size(self, name, path):
        try:
            img = Image.open(path)
        except FileNotFoundError:
            self.stdout.write(
                style.WARNING(
                    f"{name} screenshot file not found, skipping resize: {path}",
                ),
            )
            return
        width, height = img.size
        new_width = DJANGO_DOCS_SCREENSHOT_DATA[name]["width"]
        if width != new_width:
            new_height = int(height * (new_width / width))
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.save(path)
