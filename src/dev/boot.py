#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file sets up and configures Django. It's used by scripts that need to
execute as if running in a Django server.
"""

import subprocess
from os import environ
from pathlib import Path
from sys import path

import click
import django
from click.decorators import help_option
from django.conf import settings
from django.core.management import call_command


def boot_django(app: str = ""):
    BASE_DIR = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
    path.append(BASE_DIR)

    if app:
        INSTALLED_APPS = (
            "django.contrib.auth",
            "django.contrib.contenttypes",
            app,
        )
    else:
        INSTALLED_APPS = (
            "django.contrib.auth",
            "django.contrib.contenttypes",
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
    help="Make migrations",
    default=True,
    show_default=True,
)
@click.option("-M", "service", flag_value="migrate", help="Migrate")
@click.option("-s", "service", flag_value="shell", help="Run Django shell")
@click.option("-a", "service", flag_value="startapp", help="Create Application")
@click.option(
    "-n",
    "application_name",
    help="The name of the application or DEVAPP_NAME env variable.",
    envvar="DEVAPP_NAME",
    required=True,
    # default=lambda: environ.get("DEVAPP_NAME", ""),
    # prompt=True,
)
def control(application_name, service):

    if service == "migrate":
        boot_django(application_name)
        call_command("migrate")
    elif service == "shell":
        boot_django(application_name)
        call_command("shell")
    elif service == "startapp":
        boot_django()
        call_command("startapp", application_name)
    else:
        boot_django(application_name)
        call_command("makemigrations", application_name)
