from abc import ABC, abstractmethod
from typing import Any, Dict
from ..prompters.configer import PrompterConfiger
import importlib


def schemaPrompter(prompter: PrompterConfiger):
    pass


def load_extension(name: str, prompter: PrompterConfiger):
    module = importlib.import_module(f"schemdule.extensions.{name}.__reg__")
    configFuncName = "schemaPrompter"
    if hasattr(module, configFuncName):
        func = getattr(module, configFuncName)
        func(prompter)
