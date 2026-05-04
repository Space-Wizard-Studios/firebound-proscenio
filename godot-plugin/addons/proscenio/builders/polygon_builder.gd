@tool
extends RefCounted


static func attach_sprites(skeleton: Skeleton2D, sprites_data: Array) -> void:
	for sprite_data in sprites_data:
		var poly := Polygon2D.new()
		poly.name = sprite_data.get("name", "sprite")

		var polygon_pts: Array = sprite_data.get("polygon", [])
		var pts := PackedVector2Array()
		for p in polygon_pts:
			pts.append(Vector2(p[0], p[1]))
		poly.polygon = pts

		var uv_pts: Array = sprite_data.get("uv", [])
		var uvs := PackedVector2Array()
		for u in uv_pts:
			uvs.append(Vector2(u[0], u[1]))
		poly.uv = uvs

		var bone_name: String = sprite_data.get("bone", "")
		var parent: Node = skeleton
		if bone_name != "":
			var found := skeleton.find_child(bone_name, true, false)
			if found:
				parent = found
		parent.add_child(poly)
