"""Blender operators."""

from pathlib import Path
from typing import ClassVar

import bpy
from bpy.props import FloatProperty, StringProperty
from bpy_extras.io_utils import ExportHelper


class PROSCENIO_OT_smoke_test(bpy.types.Operator):
    """Smoke test operator — confirms the addon registers and dispatches."""

    bl_idname = "proscenio.smoke_test"
    bl_label = "Hello Proscenio"
    bl_description = "Print a sanity check to the system console"
    bl_options: ClassVar[set[str]] = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        message = "Proscenio smoke test OK"
        self.report({"INFO"}, message)
        print(f"[Proscenio] {message}")
        return {"FINISHED"}


class PROSCENIO_OT_export_godot(bpy.types.Operator, ExportHelper):
    """Export the active scene as a `.proscenio` JSON document."""

    bl_idname = "proscenio.export_godot"
    bl_label = "Export Proscenio (.proscenio)"
    bl_description = "Write the active scene to a Proscenio JSON file"
    bl_options: ClassVar[set[str]] = {"REGISTER"}

    filename_ext = ".proscenio"
    filter_glob: StringProperty(default="*.proscenio", options={"HIDDEN"})  # type: ignore[valid-type]

    pixels_per_unit: FloatProperty(  # type: ignore[valid-type]
        name="Pixels per unit",
        description="Conversion ratio between Blender units and Godot pixels",
        default=100.0,
        min=0.0001,
    )

    def execute(self, context: bpy.types.Context) -> set[str]:
        from ..exporters.godot import writer  # type: ignore[import-not-found]

        try:
            writer.export(self.filepath, pixels_per_unit=self.pixels_per_unit)
        except Exception as exc:
            self.report({"ERROR"}, f"Proscenio export failed: {exc}")
            return {"CANCELLED"}

        path = Path(self.filepath)
        self.report({"INFO"}, f"Proscenio: wrote {path.name}")
        print(f"[Proscenio] exported → {path}")
        return {"FINISHED"}


_classes: tuple[type, ...] = (
    PROSCENIO_OT_smoke_test,
    PROSCENIO_OT_export_godot,
)


def register() -> None:
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
