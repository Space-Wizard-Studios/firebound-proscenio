@tool
extends RefCounted


static func build(animations_data: Array) -> AnimationPlayer:
	var player := AnimationPlayer.new()
	player.name = "AnimationPlayer"

	var library := AnimationLibrary.new()

	for anim_data in animations_data:
		var anim := Animation.new()
		anim.length = float(anim_data.get("length", 1.0))
		anim.loop_mode = (
			Animation.LOOP_LINEAR
			if bool(anim_data.get("loop", false))
			else Animation.LOOP_NONE
		)
		# Track wiring (bone_transform, sprite_frame, slot_attachment, visibility)
		# lands during Phase 1 finalization. Until then, animations are
		# created empty so the player and library structure is in place.
		library.add_animation(anim_data.get("name", "anim"), anim)

	player.add_animation_library("", library)
	return player
