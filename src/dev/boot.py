#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file sets up and configures Django. It's used by scripts that need to
execute as if running in a Django server.
"""

import subprocess
from pathlib import Path
from sys import path
from typing import Optional

import click
import django
from django.conf import settings
from django.core.management import call_command


def boot_django(app: Optional[str] = "") -> None:
    BASE_DIR = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
    path.append(BASE_DIR)

    INSTALLED_APPS = tuple(
        filter(
            None,
            [
                "django.contrib.auth",
                "django.contrib.contenttypes",
                app,
            ],
        )
    )

    settings.configure(
        BASE_DIR=Path(BASE_DIR) / Path("people"),
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": Path(BASE_DIR) / Path("db.sqlite3"),
            }
        },
        INSTALLED_APPS=INSTALLED_APPS,
        TIME_ZONE="UTC",
        USE_TZ=True,
    )

    django.setup()


@click.command()
@click.option(
    "-m",
    "service",
    flag_value="makemigrations",
    help="Make Migrations",
    default=True,
    show_default=True,
)
@click.option("-M", "service", flag_value="migrate", help="Migrate")
@click.option("-s", "service", flag_value="shell", help="Run Django Shell")
@click.option("-a", "service", flag_value="startapp", help="Create Application")
@click.option("-b", "service", flag_value="build", help="Build Application")
@click.option("-pp", "service", flag_value="pypi", help="Upload to Pypi")
@click.option(
    "-n",
    "application_name",
    help="The name of the application or DEVAPP_NAME env variable.",
    envvar="DEVAPP_NAME",
    required=True,
)
def control(application_name: str, service: str) -> None:
    services = {
        "build": {
            "commands": [subprocess.run],
            "args": [[["python3", "-m", "build"]]],
        },
        "pypi": {
            "commands": [subprocess.run],
            "args": [[["twine", "upload", "dist/*"]]],
        },
        "startapp": {
            "commands": [boot_django, call_command],
            "args": [[], [service, application_name]],
        },
        "makemigrations": {
            "commands": [boot_django, call_command],
            "args": [[application_name], [service, application_name]],
        },
        "migrate": {
            "commands": [boot_django, call_command],
            "args": [[application_name], [service, application_name]],
        },
        "shell": {
            "commands": [boot_django, call_command],
            "args": [[application_name], [service]],
        }
    }

    for each_command in zip(services[service]["commands"], services[service]["args"]):
        each_command[0](*each_command[1])
