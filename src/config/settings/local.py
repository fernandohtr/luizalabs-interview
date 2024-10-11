import os

from config.settings.base import *  # noqa

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "7TQK-V4W9HZoRTcfVNfq4L5HVzDizjvnxPtyM4fdoPo2bezVON5bqA")
DEBUG = True
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]
