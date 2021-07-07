from typing import Optional
import click
import logging
from datetime import time
from .timetable import TimeTable


def demo():
    print("""
Please give a schema file:

    $ python -m schemdule --schema schema.py

An example schema file (in Python):

    at("6:30", "Get up")
    cycle("8:00", "12:00", "00:30:00", "00:10:00", "Working")

Type annotions:

    from typing import Callable
    # def at(time_str: str, message: str): ...
    at: Callable[[str, str], None]
    # def cycle(start_str: str, end_str: str, work_duration_str: str, rest_duration_str: str, message: str): ...
    cycle: Callable[[str, str, str, str, str], None]
""")


@click.command()
@click.option("--schema", default=None, help="Schema file name.")
def main(schema: Optional[str] = None) -> None:
    """Schemdule."""
    logger = logging.getLogger("main")

    print("Welcome to Schemdule!")

    if schema is not None:
        with open(schema, encoding="utf8") as f:
            src = "".join(f.readlines())
        tt = TimeTable()
        tt.load(src)
        tt.schedule()
    else:
        demo()


if __name__ == '__main__':
    main()
