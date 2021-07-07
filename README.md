# Schemdule

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/dm/schemdule)](https://pypi.org/project/schemdule/)

[Schemdule](https://github.com/StardustDL/schemdule) is a tiny tool using script for schema to schedule one day and remind you to do something during a day.

## Usage

### Write a Schema

It's a pure python script, so you can use any python statement in it.

Schemdule provide `at` and `cycle` functions for registering events.

```python
# time_str can be {hh:mm} or {hh:mm:ss}

def at(time_str: str, message: str):
    # register an event at time with message
    ...

def cycle(start_str: str, end_str: str, work_duration_str: str, rest_duration_str: str, message: str):
    # register a series of events in cycle during start to end
    # the duration of one cycle = work_duration + rest_duration
    # For each cycle, register 3 event: cycle starting, cycle resting, cycle ending
    ...
```

An example schema.

```python
# Type annotions
from typing import Callable
at: Callable[[str, str], None]
cycle: Callable[[str, str, str, str, str], None]

# Schema
at("6:30", "Get up")
cycle("8:00", "12:00", "00:30:00", "00:10:00", "Working")
```

### Run

```sh
$ python -m schemdule --schema schema.py
```
