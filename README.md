# Schemdule

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/v/schemdule.svg?logo=pypi)](https://pypi.org/project/schemdule/) ![](https://img.shields.io/pypi/dm/schemdule?logo=pypi)

[Schemdule](https://github.com/StardustDL/schemdule) is a tiny tool using script as schema to schedule one day and remind you to do something during a day.

- Platform ![](https://img.shields.io/badge/Linux-yes-success?logo=linux) ![](https://img.shields.io/badge/Windows-yes-success?logo=windows) ![](https://img.shields.io/badge/MacOS-yes-success?logo=apple) ![](https://img.shields.io/badge/BSD-yes-success?logo=freebsd)
- Python ![](https://img.shields.io/pypi/implementation/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/pyversions/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/wheel/schemdule.svg?logo=pypi)
- [All extensions](https://pypi.org/search/?q=schemdule)

## Usage

```sh
$ pip install schemdule
```

### Write a Schema

It's a pure python script, so you can use any python statement in it.

Schemdule provide `at`, `cycle`, `load` and `ext` functions for registering events, and a `PrompterConfiger` variable named `prompter` to config prompter (the default prompter is Tkinter messagebox).

```python
# raw_time can be {hh:mm} or {hh:mm:ss} or a datetime.time object

def at(raw_time: Union[str, time], message: str = "", payload: Any = None):
    # register an event at time with message
    ...

def cycle(raw_start: Union[str, time], raw_end: Union[str, time], raw_work_duration: Union[str, time], raw_rest_duration: Union[str, time], message: str = "", payload: Any = None):
    # register a series of events in cycle during start to end
    # the duration of one cycle = work_duration + rest_duration
    # For each cycle, register 2 event: cycle starting, cycle resting
    ...

def load(source: str) -> None:
    # load from a schema source code
    ...

def ext(name: str) -> None:
    # use an extension
    # provided by packages `schemdule-extensions-{extension name}`
    ...

# the class of the variable `prompter`

class PrompterConfiger:
    def use(self, prompter: Prompter) -> "PrompterConfiger": ...

    def useBroadcaster(self) -> "PrompterConfiger": ...

    def useSwitcher(self) -> "PrompterConfiger": ...

    def useConsole(self) -> "PrompterConfiger": ...

    def useTkinterMessageBox(self) -> "PrompterConfiger": ...

```

An example schema.

```python
# Type annotions
from typing import Callable, Union, Any
from datetime import time
from schemdule.prompters.configer import PrompterConfiger
from schemdule.prompters import Prompter, PrompterHub
at: Callable[[Union[str, time], str, Any], None]
cycle: Callable[[Union[str, time], Union[str, time], Union[str, time], Union[str, time], str, Any], None]
load: Callable[[str], None]
ext: Callable[[str], None]
prompter: PrompterConfiger

# Schema
at("6:30", "Get up")
cycle("8:00", "12:00", "00:30:00", "00:10:00", "Working")
# Import other schema by `load` function
# with open("other_schema.py", encoding="utf8") as f:
    # load(f.read())

prompter.useTkinterMessageBox()
# use multiple prompter:
# ext("simplegui") # use simplegui extension (package schemdule-extensions-simplegui)
# prompter.useBroadcaster().useConsole().useMessageBox(True)
```

The built timetable is like the following one.

```
Get up @ 06:30:00
Working (cycle 1 starting) @ 08:00:00
Working (cycle 1 resting starting) @ 08:30:00
Working (cycle 2 starting) @ 08:40:00
Working (cycle 2 resting starting) @ 09:10:00
Working (cycle 3 starting) @ 09:20:00
Working (cycle 3 resting starting) @ 09:50:00
Working (cycle 4 starting) @ 10:00:00
Working (cycle 4 resting starting) @ 10:30:00
Working (cycle 5 starting) @ 10:40:00
Working (cycle 5 resting starting) @ 11:10:00
Working (cycle 6 starting) @ 11:20:00
Working (cycle 6 resting starting) @ 11:50:00
```

### Run

```sh
# load and run from the schema
schemdule run schema.py
# or use python
# python -m schemdule run schema.py

# preview the built timetable
schemdule run schema.py --preview

# try the builtin demo (just for testing)
schemdule demo
```
