from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Dict
import importlib


def schemaEnvironment(env: Dict[str, Any]) -> None:
    pass


def import_extension(full_name: str) -> ModuleType:
    return importlib.import_module(f"{full_name}.__reg__")


def load_extension(name: str) -> ModuleType:
    return import_extension(f"schemdule.extensions.{name}")


def use_extension(extension: ModuleType, env: Dict[str, Any]) -> None:
    configFuncName = "schemaEnvironment"
    if hasattr(extension, configFuncName):
        func = getattr(extension, configFuncName)
        func(env)
