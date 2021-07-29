from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Dict
from ..prompters.configer import PrompterConfiger
import importlib


def schemaPrompter(prompter: PrompterConfiger) -> None:
    pass


def import_extension(full_name: str) -> ModuleType:
    return importlib.import_module(f"{full_name}.__reg__")


def load_extension(name: str) -> ModuleType:
    return import_extension(f"schemdule.extensions.{name}")


def use_extension(extension: ModuleType, env: Dict[str, Any]) -> None:
    configFuncName = "schemaPrompter"
    if hasattr(extension, configFuncName):
        func = getattr(extension, configFuncName)
        prompter = env["prompter"]
        assert isinstance(prompter, PrompterConfiger)
        func(prompter)
