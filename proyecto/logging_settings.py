import os

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s %(message)s"}
    },
    "handlers": {
        "default": {"level": "ERROR", "class": "logging.StreamHandler"},
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "tmp/django.log",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
