from typing import Optional
import click
import logging
import enlighten
import time
from .timetable import TimeTable


def demo():
    click.echo("""
Please give a schema file:

    $ python -m schemdule --schema schema.py
""")

    demo_schema = """
from datetime import datetime, timedelta
now = datetime.now()
at((now + timedelta(seconds=3)).time(), "Demo event")
cycle((now + timedelta(seconds=5)).time(), 
    (now + timedelta(seconds=20)).time(),
    (now + timedelta(seconds=5)).time(),
    (now + timedelta(seconds=5)).time(), "Demo cycle")
"""

    click.echo("A demo schema:\n")
    click.echo("\n".join(map(lambda x: "    " + x, demo_schema.strip().splitlines())))

    click.echo("\nScheduling...")

    tt = TimeTable()
    tt.load(demo_schema)

    from .prompters.general import ConsolePrompter

    tt.schedule(ConsolePrompter())


@click.command()
@click.option("--schema", default=None, help="Schema file name.")
def main(schema: Optional[str] = None) -> None:
    """Schemdule (https://github.com/StardustDL/schemdule)."""
    logger = logging.getLogger("main")

    click.echo("Welcome to Schemdule!")

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
