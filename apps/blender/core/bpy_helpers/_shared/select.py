"""bpy-bound selection helpers.

Replaces the 5+ inline copies of the deselect-all-then-select-one
idiom across operators (select_issue_object, select_outliner_object,
create_ortho_camera, reproject_sprite_uv, create_slot, etc).

Lives in ``core/`` for now; will move to ``core/bpy_helpers/`` once
the code-modularity split lands. The bpy import here is intentional and acknowledged
via the file docstring rather than the package-level "bpy-free"
contract.
"""

from __future__ import annotations

import contextlib

import bpy


def select_only(context: bpy.types.Context, obj: bpy.types.Object) -> None:
    """Deselect everything in the scene, then select + activate ``obj``.

    Mirrors the pattern Blender's UI uses for Outliner-driven
    activation: a single click selects exactly one object and makes it
    active. Suitable for operator paths that want the post-selection
    state to be unambiguous (the selected object is always the active
    one).
    """
    for other in context.scene.objects:
        other.select_set(False)
    obj.select_set(True)
    context.view_layer.objects.active = obj


def restore_selection(
    context: bpy.types.Context,
    prior_selected_names: list[str],
    prior_active: bpy.types.Object | None,
) -> None:
    """Restore a captured selection: deselect the current selection, reselect
    ``prior_selected_names`` by name, then restore ``prior_active``.

    Each step suppresses the ``RuntimeError`` / ``ReferenceError`` a stale
    (undo-recreated or deleted) datablock raises, so a partial restore never
    aborts a modal operator's ``finally`` cleanup. Object lookups go by name
    so undo-driven recreation does not strand the restore on a dead pointer.
    """
    for obj in list(context.selected_objects):
        with contextlib.suppress(RuntimeError, ReferenceError):
            obj.select_set(False)
    for name in prior_selected_names:
        obj = bpy.data.objects.get(name)
        if obj is not None:
            with contextlib.suppress(RuntimeError):
                obj.select_set(True)
    if prior_active is not None:
        with contextlib.suppress(RuntimeError, ReferenceError):
            context.view_layer.objects.active = prior_active
