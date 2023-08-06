"""Monkey-patching contextlib."""

from packaging import version
import platform
from .logging import logger

logger.warn_module_move("mt.base.contextlib", "contextlib")

if version.parse(platform.python_version()) < version.parse("3.7"):
    raise NotImplementedError(
        "Since version 3, mtbase requires Python at least version 3.7. Please upgrade."
    )

from contextlib import *
