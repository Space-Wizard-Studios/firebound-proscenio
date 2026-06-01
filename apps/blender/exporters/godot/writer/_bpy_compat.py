"""Stub-bug shims for the writer.

fake-bpy-module-latest ships PEP 561 stubs but omits ``__iter__`` and
``__getitem__`` declarations on the bpy_prop_collection wrappers
(SceneObjects, ArmatureBones, MeshVertices, etc). Those collections
ARE iterable and indexable at runtime; the stub generator just loses
the magic methods because they live on the C-level base class
``bpy_prop_collection`` which is not surfaced in the .pyi tree.

The shims here are the single place we acknowledge the gap. Each
helper takes the collection by Iterable / Sequence Protocol so the
writer's iteration sites stay readable, and casts internally so the
stub-blind region is one well-named function instead of a `cast`
sprinkled at every loop.

When fake-bpy fixes the upstream stubs, delete this module and inline
the iteration.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TypeVar, cast

import bpy

_T = TypeVar("_T")


def iter_objects(scene: bpy.types.Scene) -> Iterator[bpy.types.Object]:
    """Iterate ``scene.objects`` (stub omits __iter__ on SceneObjects)."""
    return iter(cast(Iterator[bpy.types.Object], scene.objects))


def iter_materials() -> Iterator[bpy.types.Material]:
    """Iterate ``bpy.data.materials`` (stub omits __iter__ on BlendDataMaterials)."""
    return iter(cast(Iterator[bpy.types.Material], bpy.data.materials))


def iter_actions() -> Iterator[bpy.types.Action]:
    """Iterate ``bpy.data.actions`` (stub omits __iter__ on BlendDataActions)."""
    return iter(cast(Iterator[bpy.types.Action], bpy.data.actions))


def iter_bones(armature: bpy.types.Armature) -> Iterator[bpy.types.Bone]:
    """Iterate ``armature.bones`` (stub omits __iter__ on ArmatureBones)."""
    return iter(cast(Iterator[bpy.types.Bone], armature.bones))


def iter_vertex_groups(obj: bpy.types.Object) -> Iterator[bpy.types.VertexGroup]:
    """Iterate ``obj.vertex_groups`` (stub omits __iter__ on VertexGroups)."""
    return iter(cast(Iterator[bpy.types.VertexGroup], obj.vertex_groups))


def vertex_at(mesh: bpy.types.Mesh, index: int) -> bpy.types.MeshVertex:
    """Subscript ``mesh.vertices[index]`` (stub omits __getitem__ on MeshVertices)."""
    return cast(bpy.types.MeshVertex, mesh.vertices[index])  # type: ignore[index]


def polygon_at(mesh: bpy.types.Mesh, index: int) -> bpy.types.MeshPolygon:
    """Subscript ``mesh.polygons[index]`` (stub omits __getitem__ on MeshPolygons)."""
    return cast(bpy.types.MeshPolygon, mesh.polygons[index])  # type: ignore[index]


def vertex_group_at(obj: bpy.types.Object, index: int) -> bpy.types.VertexGroup:
    """Subscript ``obj.vertex_groups[index]`` (stub omits __getitem__ on VertexGroups)."""
    return cast(bpy.types.VertexGroup, obj.vertex_groups[index])  # type: ignore[index]


def iter_action_layers(action: bpy.types.Action) -> Iterator[bpy.types.ActionLayer]:
    """Iterate ``action.layers`` (stub omits __iter__ on ActionLayers)."""
    return iter(cast(Iterator[bpy.types.ActionLayer], action.layers))


def iter_action_strips(layer: bpy.types.ActionLayer) -> Iterator[bpy.types.ActionStrip]:
    """Iterate ``layer.strips`` (stub omits __iter__ on ActionStrips)."""
    return iter(cast(Iterator[bpy.types.ActionStrip], layer.strips))


def iter_shader_nodes(tree: bpy.types.NodeTree) -> Iterator[bpy.types.Node]:
    """Iterate ``tree.nodes`` (stub omits __iter__ on Nodes)."""
    return iter(cast(Iterator[bpy.types.Node], tree.nodes))


def iter_poly_vertices(poly: bpy.types.MeshPolygon) -> Iterator[int]:
    """Iterate ``poly.vertices`` (bpy_prop_array carries no Iterable in stub)."""
    return iter(cast(Iterator[int], poly.vertices))


def iter_poly_loop_indices(poly: bpy.types.MeshPolygon) -> Iterator[int]:
    """Iterate ``poly.loop_indices`` (bpy_prop_array carries no Iterable in stub)."""
    return iter(cast(Iterator[int], poly.loop_indices))


def iter_keyframe_points(
    fcurve: bpy.types.FCurve,
) -> Iterator[bpy.types.Keyframe]:
    """Iterate ``fcurve.keyframe_points`` (stub omits __iter__ on FCurveKeyframePoints)."""
    return iter(cast(Iterator[bpy.types.Keyframe], fcurve.keyframe_points))


def expect_mesh(obj: bpy.types.Object) -> bpy.types.Mesh:
    """Narrow ``obj.data`` to ``bpy.types.Mesh`` when ``obj.type == 'MESH'``.

    The stub types ``Object.data`` as a 12-way union over every ID datablock
    Blender allows on an object. Callers in the writer have already filtered
    on ``obj.type``; this helper just satisfies the type system by asserting
    the narrowing the runtime contract already guarantees.
    """
    data = obj.data
    if not isinstance(data, bpy.types.Mesh):
        raise TypeError(f"expected Mesh on object {obj.name!r}, got {type(data).__name__}")
    return data


def expect_armature(obj: bpy.types.Object) -> bpy.types.Armature:
    """Narrow ``obj.data`` to ``bpy.types.Armature`` when ``obj.type == 'ARMATURE'``."""
    data = obj.data
    if not isinstance(data, bpy.types.Armature):
        raise TypeError(f"expected Armature on object {obj.name!r}, got {type(data).__name__}")
    return data
