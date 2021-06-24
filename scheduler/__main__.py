from typing import Optional
import click
import logging
from datetime import time
from .timetable import TimeTable, schedule, timetable_from_source


def demo():
    print("DEMO")

    tt = TimeTable()
    tt.at(time(1, 2), "abc")
    tt.at(time(1, 2), "def")

    schedule(tt)

    schedule(timetable_from_source("""
at("1:2:30:40", "message")
"""))


@click.command()
@click.option("--schema", default=None, help="File name.")
def main(schema: Optional[str] = None) -> None:
    """Scheduler."""
    logger = logging.getLogger("main")

    print("Welcome to Scheduler!")

    if schema is not None:
        with open(schema) as f:
            src = "".join(f.readlines())
        tt = timetable_from_source(src)
        schedule(tt)
    else:
        demo()


if __name__ == '__main__':
    main()
