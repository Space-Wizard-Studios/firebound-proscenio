"""Blender operators."""

import bpy


class PROSCENIO_OT_smoke_test(bpy.types.Operator):
    """Smoke test operator — confirms the addon registers and dispatches."""

    bl_idname = "proscenio.smoke_test"
    bl_label = "Hello Proscenio"
    bl_description = "Print a sanity check to the system console"
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        message = "Proscenio smoke test OK"
        self.report({"INFO"}, message)
        print(f"[Proscenio] {message}")
        return {"FINISHED"}


_classes: tuple[type, ...] = (PROSCENIO_OT_smoke_test,)


def register() -> None:
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
