"""Doctor related commands.

Commands invoked by dpteam doctor <some-command> is defined here.
"""

import subprocess
from sys import platform

import click
import questionary as q
from rich.console import Console
from rich.style import Style


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "error": Style(color="red", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


@click.command()
def doctor() -> None:
    """Doctor command."""
    skipped_dependencies = False

    console.print("Checking for uninstalled dependencies...", style=styles["normal"])

    if platform == "darwin":

        brew_installation = subprocess.run(["brew", "--help"], capture_output=True, text=True, shell=False)

        if brew_installation.stderr:
            console.print("We have detected that you are using MacOS but seem to be missing Homebrew...🍺", style=styles["normal"])
            console.print(
                "Please install Homebrew and verify your installation by running 'brew doctor'. Then rerun this command.",
                style=styles["normal"],
            )

            exit(1)

        else:

            gcloud_installation = subprocess.run(["gcloud", "--help"], capture_output=True, text=True, shell=False)

            if not gcloud_installation.stderr:
                console.print("The 'gcloud' CLI tool is required but seems to be missing.", style=styles["normal"])
                gcloud_permission = q.confirm("Permission to install 'gcloud'? ").ask()

                if gcloud_permission:

                    console.print("Installing Google Cloud CLI...", style=styles["normal"])

                    gcloud_installer = subprocess.run(
                        ["brew", "install", "--cask", "google-cloud-sdk"], capture_output=False, text=True, shell=False
                    )

                    if gcloud_installer.stderr:
                        console.print("Something went wrong when trying to install gcloud with Homebrew...", style=styles["error"])

                        exit(1)

                else:
                    skipped_dependencies = True

        if skipped_dependencies:
            console.print(
                "You skipped installing some dependencies. You need to install them to use some CLI commands...",
                style=styles["warning"],
            )
        else:
            console.print("Everything seems to be ok ✅ The CLI is good to go.", style=styles["success"])
