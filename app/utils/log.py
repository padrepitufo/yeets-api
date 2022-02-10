from logging import (
    getLogger,
    Formatter,
    StreamHandler,
)

from utils import config


LEVEL = config.LOG_LEVEL
FORMAT = config.LOG_FORMAT


def setup():
    console = StreamHandler()
    console.setLevel(LEVEL)
    formatter = Formatter(FORMAT)
    console.setFormatter(formatter)
    getLogger("").addHandler(console)