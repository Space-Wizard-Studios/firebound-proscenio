"""Blender UI panels."""

import bpy


class PROSCENIO_PT_main(bpy.types.Panel):
    """Main Proscenio sidebar panel in the 3D Viewport."""

    bl_label = "Proscenio"
    bl_idname = "PROSCENIO_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Proscenio"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.label(text="Pipeline v0.1.0", icon="INFO")
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Export")
        col.operator("proscenio.export_godot", icon="EXPORT")
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Diagnostics")
        col.operator("proscenio.smoke_test", icon="PLAY")


_classes: tuple[type, ...] = (PROSCENIO_PT_main,)


def register() -> None:
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
