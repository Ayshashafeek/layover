"""Logging helpers.

Small wrapper so every route/service logs through one place. Uses
standard-library logging: `logging.getLogger("app.<name>")` in handlers.
"""

import logging

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"app.{name}")
