# schemdule-extensions-simplegui

![](https://github.com/StardustDL/schemdule/workflows/CI/badge.svg) ![](https://img.shields.io/github/license/StardustDL/schemdule.svg) [![](https://img.shields.io/pypi/v/schemdule-extensions-simplegui.svg?logo=pypi)](https://pypi.org/project/schemdule-extensions-simplegui/) [![Downloads](https://pepy.tech/badge/schemdule-extensions-simplegui)](https://pepy.tech/project/schemdule-extensions-simplegui)

A simple GUI extension for 
[Schemdule](https://github.com/StardustDL/schemdule).

- Platform ![](https://img.shields.io/badge/Linux-yes-success?logo=linux) ![](https://img.shields.io/badge/Windows-yes-success?logo=windows) ![](https://img.shields.io/badge/MacOS-yes-success?logo=apple) ![](https://img.shields.io/badge/BSD-yes-success?logo=freebsd)
- Python ![](https://img.shields.io/pypi/implementation/schemdule-extensions-simplegui.svg?logo=pypi) ![](https://img.shields.io/pypi/pyversions/schemdule-extensions-simplegui.svg?logo=pypi) ![](https://img.shields.io/pypi/wheel/schemdule-extensions-simplegui.svg?logo=pypi)
- [All extensions](https://pypi.org/search/?q=schemdule)

## Install

Use pip:

```sh
pip install schemdule-extensions-simplegui
```

Or use pipx:

```sh
pipx inject schemdule schemdule-extensions-simplegui

# Upgrade
pipx upgrade schemdule --include-injected
```

Check if the extension installed:

```sh
schemdule ext
```

## Usage

This extension provide a `MessageBoxPrompter` and add the following extension methods on `PrompterBuilder`.

```python
class PrompterBuilder:
    def useMessageBox(self, auto_close: bool = False, final: bool = False) -> "PrompterBuilder":
        ...
```

Use the extension in the schema script.

```python
# schema.py
ext("simplegui")

prompter.useMessageBox()
```

