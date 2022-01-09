#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file sets up and configures Django. It's used by scripts that need to
execute as if running in a Django server.
"""

import subprocess
from pathlib import Path
from sys import path

import click
from click.decorators import help_option
import django
from django.conf import settings
from django.core.management import call_command


def boot_django(app: str):
    BASE_DIR = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
    path.append(BASE_DIR)

    settings.configure(
        BASE_DIR=Path(BASE_DIR) / Path("people"),
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": Path(BASE_DIR) / Path("db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            app,
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()


@click.command()
@click.option("--service", "-s",
              default="makemigrations",
              help="Specify service to run: (makemigrations(default), migrate, shell)")
@click.argument("application_name", nargs=1)
def control(application_name, service):
    boot_django(application_name)
    if service == "migrate":
        call_command("migrate")
    elif service == "shell":
        call_command("shell")
    else:
        call_command("makemigrations", application_name)
