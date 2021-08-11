import logging
import time
from typing import Optional

import click

import enlighten

from . import __version__
from .helpers import buildMessage
from .schedulers import Scheduler
from .schemas import SchemaBuilder
from .schemas.timetable import TimeTable


def previewTimeTable(timetable: TimeTable, scheduler: Scheduler):
    for item in scheduler.scheduledTimeTable(timetable):
        click.echo(buildMessage(item))


@click.command()
def demo():
    """Try a schema scheduling demo."""
    click.echo("""
Please give a schema file:

    $ python -m schemdule --schema schema.py
""")

    demo_schema = """
from datetime import datetime, timedelta
now = datetime.now()
now = now - timedelta(microseconds=now.microsecond)

def callable_payload():
    print("From Callable")

at((now + timedelta(seconds=1)).time(), "Demo event", callable_payload)

at((now + timedelta(seconds=3)).time(), "Demo event")

cycle((now + timedelta(seconds=5)).time(), 
    (now + timedelta(seconds=20)).time(),
    "00:00:05",
    "00:00:05", "Demo cycle")

prompter.clear().useSwitcher().useConsole().useCallable()
"""
    click.echo("A demo schema:\n")
    click.echo("\n".join(map(lambda x: "    " + x,
                        demo_schema.strip().splitlines())))

    tt = SchemaBuilder()

    tt.load(demo_schema)

    click.echo("Built timetable:\n")

    sc = Scheduler()

    previewTimeTable(tt.result, sc)

    click.echo("\nScheduling...\n")

    sc.schedule(tt.result)


@click.command()
@click.option("--preview", is_flag=True, default=False, help="Preview the built timetable.")
@click.argument("schema", type=click.Path(exists=True))
def run(schema: str, preview: bool = False) -> None:
    """Schedule a schema."""
    logger = logging.getLogger("run")

    tt = SchemaBuilder()

    with open(schema, encoding="utf8") as f:
        tt.load(f.read())

    sc = Scheduler()

    if preview:
        previewTimeTable(tt.result, sc)
    else:
        sc.schedule(tt.result)


@click.command()
def ext() -> None:
    """List all installed extensions."""
    logger = logging.getLogger("ext")

    from .extensions import findExtensions, loadExtension, getExtensionMetadata

    extnames = findExtensions()

    click.echo(f"Found {len(extnames)} extension(s).")

    for name in extnames:
        ext = loadExtension(name)
        metadata = getExtensionMetadata(ext)
        click.echo(f"  {name} v{metadata['version']}")


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-v', '--verbose', count=True, default=0, type=click.IntRange(0, 4))
@click.option("--version", is_flag=True, default=False, help="Show the version.")
def main(ctx=None, verbose: int = 0, version: bool = False) -> None:
    """Schemdule (https://github.com/StardustDL/schemdule)

A tiny tool using script as schema to schedule one day and remind you to do something during a day.
"""
    click.echo(f"Welcome to Schemdule v{__version__}!")

    logger = logging.getLogger("Cli-Main")

    loggingLevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: logging.NOTSET
    }[verbose]

    logging.basicConfig(level=loggingLevel)

    logger.debug(f"Logging level: {loggingLevel}")

    if version:
        click.echo(f"Schemdule v{__version__}")
        exit(0)


main.add_command(run)
main.add_command(demo)
main.add_command(ext)

if __name__ == '__main__':
    main()
