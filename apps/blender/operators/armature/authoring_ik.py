"""IK chain toggle authoring shortcut (the authoring panel.1.b)."""

from __future__ import annotations

from typing import ClassVar

import bpy
from bpy.props import IntProperty
from mathutils import Vector

from ...core._shared.report import report_info  # type: ignore[import-not-found]

_IK_CONSTRAINT_NAME = "Proscenio IK"
_IK_TARGET_SUFFIX = ".IK"
_MIN_TARGET_SIZE = 0.1


def _ik_target_name(bone_name: str) -> str:
    """Deterministic control-bone name for a constrained bone."""
    return f"{bone_name}{_IK_TARGET_SUFFIX}"


def _is_proscenio_target(name: str) -> bool:
    """True for a control bone this operator created, so toggle-off only ever
    deletes our own scaffolding - a hand-retargeted constraint is left alone."""
    return bool(name) and name.endswith(_IK_TARGET_SUFFIX)


def _rest_target_placement(pose_bone: bpy.types.PoseBone) -> tuple[Vector, Vector]:
    """Head/tail (armature rest space) for a control bone at the chain tip.

    The control sits at the constrained bone's rest tail so toggling IK on does
    not jump the chain; it points up the in-plane Z axis with a visible length
    derived from the source bone (floored so a zero-length bone still yields a
    selectable handle).
    """
    head = Vector(pose_bone.bone.tail_local)
    size = max(pose_bone.bone.length * 0.5, _MIN_TARGET_SIZE)
    tail = head + Vector((0.0, 0.0, size))
    return head, tail


def _create_target_bone(armature: bpy.types.Object, name: str, head: Vector, tail: Vector) -> None:
    """Create (or reposition) the non-deforming control bone in Edit Mode.

    Unparented so it floats free as the IK goal, and ``use_deform`` off so it
    never adds a vertex group to bound meshes.
    """
    bpy.ops.object.mode_set(mode="EDIT")
    try:
        edit_bones = armature.data.edit_bones
        edit_bone = edit_bones.get(name) or edit_bones.new(name)
        edit_bone.head = head
        edit_bone.tail = tail
        edit_bone.parent = None
        edit_bone.use_deform = False
    finally:
        bpy.ops.object.mode_set(mode="POSE")


def _delete_bone(armature: bpy.types.Object, name: str) -> None:
    """Remove a control bone by name in Edit Mode (no-op when absent)."""
    bpy.ops.object.mode_set(mode="EDIT")
    try:
        edit_bones = armature.data.edit_bones
        edit_bone = edit_bones.get(name)
        if edit_bone is not None:
            edit_bones.remove(edit_bone)
    finally:
        bpy.ops.object.mode_set(mode="POSE")


class PROSCENIO_OT_toggle_ik_chain(bpy.types.Operator):
    """Toggle a Proscenio-owned IK constraint on the active pose bone."""

    bl_idname = "proscenio.toggle_ik_chain"
    bl_label = "Proscenio: Toggle IK"
    bl_description = (
        "Adds an IK constraint named 'Proscenio IK' to the active pose bone "
        "(chain length 2) wired to a control bone created at the chain tip, so "
        "the chain solves on its own. Click again to remove both. Hand-added "
        "constraints and retargeted ones are left untouched."
    )
    bl_options: ClassVar[set[str]] = {"REGISTER", "UNDO"}

    chain_length: IntProperty(  # type: ignore[valid-type]
        name="Chain length",
        default=2,
        min=0,
        soft_max=8,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if context.mode != "POSE":
            return False
        bone = getattr(context, "active_pose_bone", None)
        return bone is not None

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        bone = context.active_pose_bone
        bone_name = bone.name
        existing = bone.constraints.get(_IK_CONSTRAINT_NAME)
        if existing is not None:
            subtarget = existing.subtarget
            bone.constraints.remove(existing)
            if _is_proscenio_target(subtarget):
                _delete_bone(armature, subtarget)
            report_info(self, f"removed IK from '{bone_name}'")
            return {"FINISHED"}

        target_name = _ik_target_name(bone_name)
        head, tail = _rest_target_placement(bone)
        _create_target_bone(armature, target_name, head, tail)

        # The mode round-trip can invalidate the pose-bone handle - re-fetch by name.
        pose_bone = armature.pose.bones[bone_name]
        ik = pose_bone.constraints.new(type="IK")
        ik.name = _IK_CONSTRAINT_NAME
        ik.chain_count = self.chain_length
        ik.target = armature
        ik.subtarget = target_name
        report_info(
            self,
            f"added IK to '{bone_name}' (chain={self.chain_length}) targeting '{target_name}'",
        )
        return {"FINISHED"}


_classes: tuple[type, ...] = (PROSCENIO_OT_toggle_ik_chain,)


def register() -> None:
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
