"""Proscenio Blender addon entry point.

Registers operators and panels. Real logic lives in the submodules.
"""

from . import operators, panels


def register() -> None:
    operators.register()
    panels.register()


def unregister() -> None:
    panels.unregister()
    operators.unregister()
