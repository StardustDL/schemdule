[![Schemdule](https://socialify.git.ci/StardustDL/schemdule/image?description=1&font=Bitter&forks=1&issues=1&language=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Light)](https://github.com/StardustDL/schemdule)

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/v/schemdule.svg?logo=pypi)](https://pypi.org/project/schemdule/) [![Downloads](https://pepy.tech/badge/schemdule)](https://pepy.tech/project/schemdule)

[Schemdule](https://github.com/StardustDL/schemdule) is a tiny tool using script as schema to schedule one day and remind you to do something during a day.

- Platform ![](https://img.shields.io/badge/Linux-yes-success?logo=linux) ![](https://img.shields.io/badge/Windows-yes-success?logo=windows) ![](https://img.shields.io/badge/MacOS-yes-success?logo=apple) ![](https://img.shields.io/badge/BSD-yes-success?logo=freebsd)
- Python ![](https://img.shields.io/pypi/implementation/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/pyversions/schemdule.svg?logo=pypi) ![](https://img.shields.io/pypi/wheel/schemdule.svg?logo=pypi)

![](https://raw.githubusercontent.com/StardustDL/own-staticfile-hosting/master/schemdule/terminal.png)

## Install

Use pip:

```sh
pip install schemdule
```

Or use pipx:

```sh
# Install pipx
pip install --user pipx
pipx ensurepath

# Install Schemdule
pipx install schemdule

# Install extension
pipx inject schemdule schemdule-extensions-{extension name}

# Upgrade
pipx upgrade schemdule --include-injected
```

## Usage

### Write a Schema

An example schema.

```python
# Schema
at("6:30", "Get up")
cycle("8:00", "12:00", "00:30:00", "00:10:00", "Working")
# Import other schema by `load` function
# load("other_schema.py")

prompter.useTkinterMessageBox()

# ext("simplegui") # use simplegui extension (package schemdule-extensions-simplegui)

# use multiple prompter:
# prompter.useBroadcaster().useConsole().useMessageBox(True)
```

The built timetable is like the following one from the results of the command `schemdule run schema.py --preview`.

```
🕡 06:30:00 - 🕗 08:00:00 🔔 Get up
🕗 08:00:00 - 🕣 08:30:00 💼 Working (cycle 1 starting)
🕣 08:30:00 - 🕣 08:40:00 ☕ Working (cycle 1 resting starting)
🕣 08:40:00 - 🕘 09:10:00 💼 Working (cycle 2 starting)
🕘 09:10:00 - 🕘 09:20:00 ☕ Working (cycle 2 resting starting)
🕘 09:20:00 - 🕤 09:50:00 💼 Working (cycle 3 starting)
🕤 09:50:00 - 🕙 10:00:00 ☕ Working (cycle 3 resting starting)
🕙 10:00:00 - 🕥 10:30:00 💼 Working (cycle 4 starting)
🕥 10:30:00 - 🕥 10:40:00 ☕ Working (cycle 4 resting starting)
🕥 10:40:00 - 🕚 11:10:00 💼 Working (cycle 5 starting)
🕚 11:10:00 - 🕚 11:20:00 ☕ Working (cycle 5 resting starting)
🕚 11:20:00 - 🕦 11:50:00 💼 Working (cycle 6 starting)
🕦 11:50:00 - 🕦 11:50:00 ☕ Working (cycle 6 resting starting)
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

## Schema Specification

Schema is a pure python script, so you can use any python statement in it.

Schemdule provide `at`, `cycle`, `load` and `ext` functions for registering events, and a `PrompterBuilder` variable named `prompter` to config prompter.

> These functions and variable can be accessed and modified in the variable `env`, a dict for these items provided by Schemdule. You can change the `env` variable to change the execute environment for `load` function.

```python
# raw_time can be {hh:mm} or {hh:mm:ss} or a datetime.time object

def at(rawTime: Union[str, time], message: str = "", payload: Any = None) -> None:
    # register an event at time with message
    # if payload is a PayloadBuilder, Schemdule will build the final payload automaticly
    ...

def cycle(rawStart: Union[str, time], rawEnd: Union[str, time], rawWorkDuration: Union[str, time, timedelta], rawRestDuration: Union[str, time, timedelta], message: str = "", workPayload: Optional[Callable[[int], Any]] = None, restPayload: Optional[Callable[[int], Any]] = None) -> None:
    # register a series of events in cycle during start to end
    # the duration of one cycle = workDuration + restDuration
    # For each cycle, register 2 event: cycle starting, cycle resting
    # workPayload and restPayload is the payload generator such as:
    #   def generator(index: int) -> Any: ...
    # if the returened payload is a PayloadBuilder, Schemdule will build the final payload automaticly, 
    ...


def loadRaw(source: str) -> None:
    # load from a schema source code
    ...

def load(file: str, encoding: str = "utf8") -> None:
    # load from a schema source code file
    ...

def ext(name: Optional[str] = None) -> None:
    # use an extension or use all installed extensions (if name is None)
    # provided by packages `schemdule-extensions-{extension name}`
    ...

def payloads() -> PayloadBuilder:
    # create a payload builder
    ...

def prompters() -> PrompterBuilder:
    # create a prompter builder
    ...

# the class PayloadBuilder

class PayloadBuilder:
    def use(self, payload: Any) -> "PayloadBuilder": ...

# the class of the variable `prompter`

class PrompterBuilder:
    def use(self, prompter: Prompter) -> "PrompterBuilder": ...

    def useBroadcaster(self, final: bool = False) -> "PrompterBuilder": ...

    def useSwitcher(self, final: bool = False) -> "PrompterBuilder": ...

    def useConsole(self, final: bool = False) -> "PrompterBuilder": ...

    def useCallable(self, final: bool = False) -> "PrompterBuilder": ...

    def useTkinterMessageBox(self, final: bool = False) -> "PrompterBuilder": ...

    def clear(self) -> "PrompterBuilder": ...

# the default value of the variable `prompter`

def default_prompter_builder() -> PrompterBuilder:
    prompter = PrompterBuilder()
    prompter.useSwitcher().useConsole().useCallable(True).useTkinterMessageBox()
    return prompter
```

Here are the type annotions for schema.

```python
# Type annotions
from typing import Callable, Union, Any, Dict, Optional
from datetime import time, timedelta
from schemdule.prompters.builders import PrompterBuilder, PayloadBuilder
from schemdule.prompters import Prompter, PrompterHub
at: Callable[[Union[str, time], str, Any], None]
cycle: Callable[[Union[str, time], Union[str, time], Union[str, time, timedelta], Union[str, time, timedelta], str, Optional[Callable[[int], Any]], Optional[Callable[[int], Any]]], None]
loadRaw: Callable[[str], None]
load: Callable[[str], None]
ext: Callable[[Optional[str]], None]
payloads: Callable[[], PayloadBuilder]
payloads: Callable[[], PrompterBuilder]
prompter: PrompterBuilder
env: Dict[str, Any]
```

## Extensions

- [SimpleGUI](https://github.com/StardustDL/schemdule/tree/master/src/extensions/simplegui) [![](https://img.shields.io/pypi/v/schemdule-extensions-simplegui.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-simplegui/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-simplegui)](https://pepy.tech/project/schemdule-extensions-simplegui)
- [Miaotixing](https://github.com/StardustDL/schemdule/tree/master/src/extensions/miaotixing) [![](https://img.shields.io/pypi/v/schemdule-extensions-miaotixing.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-miaotixing/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-miaotixing)](https://pepy.tech/project/schemdule-extensions-miaotixing)
- [AudioPlay](https://github.com/StardustDL/schemdule/tree/master/src/extensions/audioplay) [![](https://img.shields.io/pypi/v/schemdule-extensions-audioplay.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-audioplay/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-audioplay)](https://pepy.tech/project/schemdule-extensions-audioplay)
- [All extensions on PyPI](https://pypi.org/search/?q=schemdule)
