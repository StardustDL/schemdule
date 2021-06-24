from typing import Optional
import click
import logging
from datetime import time
from .timetable import TimeTable


def demo():
    print("DEMO")

    t1 = TimeTable()
    t1.at(time(1, 2), "abc")
    t1.at(time(1, 2), "def")

    t1.schedule()

    t2 = TimeTable()
    t2.load("""
at("1:2:30:40", "message")
""")
    t2.schedule()


@click.command()
@click.option("--schema", default=None, help="File name.")
def main(schema: Optional[str] = None) -> None:
    """Scheduler."""
    logger = logging.getLogger("main")

    print("Welcome to Scheduler!")

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
