import logging

from rich.logging import RichHandler

logging.basicConfig(
    datefmt="%H:%M:%S",
    format="%(message)s",
    handlers=[RichHandler()],
)
logs = logging.getLogger("src")


def setup_cli_logging(level: int):
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=False, show_path=False)],
    )
    logs.setLevel(level)
