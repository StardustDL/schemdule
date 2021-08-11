import importlib
import logging
import pkgutil
from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Dict, List, Set

EXTENSION_MODULE_PREFIX = "schemdule.extensions."

_logger = logging.getLogger("extensions")


def schemaEnvironment(env: Dict[str, Any]) -> None:
    pass


def findExtensions() -> List[str]:
    return [name.replace(EXTENSION_MODULE_PREFIX, "", 1) for finder, name, ispkg in pkgutil.iter_modules(__path__, EXTENSION_MODULE_PREFIX)]


def importExtension(full_name: str) -> ModuleType:
    _logger.debug(f"Import extension {full_name}.")
    return importlib.import_module(f"{full_name}.__reg__")


def loadExtension(name: str) -> ModuleType:
    _logger.info(f"Load extension {name}.")
    return importExtension(f"schemdule.extensions.{name}")


def loadExtensions(names: List[str]) -> List[ModuleType]:
    return [loadExtension(name) for name in names]


def useExtension(extension: ModuleType, env: Dict[str, Any]) -> None:
    _logger.info(
        f"Use extension {extension.__name__.replace('__reg__', '', 1)}.")
    configFuncName = "schemaEnvironment"
    if hasattr(extension, configFuncName):
        func = getattr(extension, configFuncName)
        func(env)


def useExtensions(extensions: List[ModuleType], env: Dict[str, Any]) -> None:
    for extension in extensions:
        useExtension(extension, env)


def getExtensionMetadata(extension: ModuleType) -> Dict[str, Any]:
    version = getattr(extension, "__version__", None)
    return {"version": version}
