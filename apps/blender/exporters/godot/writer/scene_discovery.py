"""Scene-walker helpers: find armature, sprite meshes, atlas image, doc name."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import bpy

from core._bpy_compat import iter_materials, iter_objects, iter_shader_nodes


def find_armature(scene: bpy.types.Scene) -> bpy.types.Object | None:
    """Return the first ARMATURE in the scene or ``None``."""
    for obj in iter_objects(scene):
        if obj.type == "ARMATURE":
            return obj
    return None


def find_sprite_meshes(scene: bpy.types.Scene) -> list[bpy.types.Object]:
    """Return every MESH in the scene, sorted by name for deterministic output."""
    sprites = [obj for obj in iter_objects(scene) if obj.type == "MESH"]
    sprites.sort(key=lambda o: o.name)
    return sprites


def find_atlas_image(out_path: Path) -> str | None:
    """Atlas filename: linked images first, sibling ``atlas.png`` fallback."""
    for image in _iter_linked_images():
        return _image_filename(image)
    sibling = out_path.parent / "atlas.png"
    return sibling.name if sibling.exists() else None


def _iter_linked_images() -> Iterator[bpy.types.Image]:
    for mat in iter_materials():
        if not mat.use_nodes or mat.node_tree is None:
            continue
        for node in iter_shader_nodes(mat.node_tree):
            if isinstance(node, bpy.types.ShaderNodeTexImage) and node.image is not None:
                yield node.image


def _image_filename(image: bpy.types.Image) -> str:
    fp = image.filepath
    return Path(bpy.path.abspath(fp)).name if fp else f"{image.name}.png"


def doc_name() -> str:
    blend = bpy.data.filepath
    return Path(blend).stem if blend else "proscenio_doc"
