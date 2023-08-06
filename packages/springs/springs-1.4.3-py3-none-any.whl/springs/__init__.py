from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from omegaconf import MISSING, DictConfig, ListConfig

from .commandline import cli
from .core import (
    cast,
    edit_list,
    from_dataclass,
    from_dict,
    from_file,
    from_none,
    from_options,
    from_string,
    merge,
    resolve,
    to_dict,
    to_yaml,
    unsafe_merge,
    validate,
)
from .flexyclasses import flexyclass
from .initialize import Target, init
from .logging import configure_logging
from .nicknames import NicknameRegistry
from .resolvers import all_resolvers, register
from .traversal import traverse
from .types import get_type
from .utils import SpringsWarnings, get_version

__version__ = get_version()


T = TypeVar("T")


def toggle_warnings(value: Optional[bool] = None):
    """Shortcut for springs.utils.SpringsWarnings.toggle"""
    SpringsWarnings.toggle(value)


def make_target(c: Callable) -> str:
    """Shortcut for springs.initialize.Target.to_string"""
    return Target.to_string(c)


def nickname(name: str) -> Callable[[Type[T]], Type[T]]:
    """Shortcut for springs.nicknames.NicknameRegistry.add"""
    return NicknameRegistry.add(name)


def make_flexy(cls_: Any) -> Any:
    """Shortcut for springs.flexyclasses.flexyclass"""

    SpringsWarnings.deprecated(
        deprecated="make_flexy",
        replacement="flexyclass",
    )
    return flexyclass(cls_)


def fdict(**kwargs: Any) -> Dict[str, Any]:
    """Shortcut for creating a Field with a default_factory that returns
    a dictionary.

    Args:
        **kwargs: values for the dictionary returned by default factory"""

    def _factory_fn() -> Dict[str, Any]:
        return {**kwargs}

    return field(default_factory=_factory_fn)


def flist(*args: Any) -> List[Any]:
    """Shortcut for creating a Field with a default_factory that returns
    a list.

    Args:
        *args: values for the list returned by default factory"""

    def _factory_fn() -> List[Any]:
        return [*args]

    return field(default_factory=_factory_fn)


__all__ = [
    "all_resolvers",
    "cast",
    "cli",
    "configure_logging",
    "dataclass",
    "DictConfig",
    "edit_list",
    "fdict",
    "field",
    "flexyclass",
    "flist",
    "from_dataclass",
    "from_dict",
    "from_file",
    "from_none",
    "from_options",
    "from_string",
    "get_type",
    "init",
    "ListConfig",
    "make_flexy",
    "make_target",
    "merge",
    "MISSING",
    "nickname",
    "register",
    "resolve",
    "Target",
    "to_dict",
    "to_yaml",
    "toggle_warnings",
    "traverse",
    "unsafe_merge",
    "validate",
]
