"""Shared status-bar chord primitive for modal operators.

A "chord" is one aligned row of icon/text labels in a modal operator's
STATUSBAR (or 3D-viewport header) hint - the bottom-bar cheatsheet that
mirrors Blender's own knife / loop-cut status bars. The per-operator
``_status_bar`` modules own their chord *vocabulary* (which gestures to
list, in what order); this module owns the one primitive that renders a
row so the icon/text layout never drifts between operators.
"""

from __future__ import annotations

import bpy


def chord(layout: bpy.types.UILayout, *parts: tuple[str, str]) -> None:
    """Emit one aligned chord row. Each part is ``(icon, text)``; an empty
    icon prints text only, an empty text prints the icon only. Uses
    Blender's native ``EVENT_*`` / ``MOUSE_*`` icons so the hint visually
    matches Blender's own modal status bars (knife / loop cut)."""
    row = layout.row(align=True)
    for icon, text in parts:
        row.label(text=text, icon=icon or "NONE")
