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
@click.option(
    "-n",
    "application_name",
    help="The name of the application or DEVAPP_NAME env variable.",
    envvar="DEVAPP_NAME",
    required=True,
)
def control(application_name: str, service: str) -> None:

    if service == "startapp":
        boot_django()
    else:
        boot_django(application_name)

    if service == "shell":
        call_command(service)
    else:
        call_command(service, application_name)
