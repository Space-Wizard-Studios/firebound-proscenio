"""Smoke test for the Sprite discriminated union (OQ3 of SPEC 014).

Covers:

- ``type`` absent -> ``PolygonSprite`` (backwards-compatible v1 path).
- ``type: "polygon"`` -> ``PolygonSprite``.
- ``type: "sprite_frame"`` -> ``SpriteFrameSprite``.
- Unknown ``type`` raises ``ValidationError``.
- Generated JSON Schema for the discriminator is wired correctly
  (carries the two variants under either a ``$ref`` chain or an
  inline ``oneOf`` / ``discriminator`` block).

Why this matters: the discriminated union is the trickiest part of
the model. If pydantic's output drifts from what downstream codegens
(``json-schema-to-typescript`` in SPEC 014 P3, the GDScript emitter
in P4) understand, every consumer breaks at once. Catch drift here
before it ripples.
"""

from __future__ import annotations

import pytest
from proscenio_codegen.schema_dump import build_proscenio_schema
from proscenio_models import PolygonSprite, ProscenioDocument, SpriteFrameSprite
from pydantic import ValidationError


def _doc_with_sprite(sprite_payload: dict) -> dict:
    return {
        "format_version": 1,
        "name": "smoke",
        "pixels_per_unit": 100.0,
        "skeleton": {"bones": [{"name": "root"}]},
        "sprites": [sprite_payload],
    }


def test_polygon_sprite_without_type_defaults_to_polygon() -> None:
    """A v1 sprite without ``type`` parses as ``PolygonSprite``."""
    payload = _doc_with_sprite(
        {
            "name": "arm",
            "texture_region": [0, 0, 1, 1],
            "polygon": [[0, 0], [1, 0], [1, 1]],
            "uv": [[0, 0], [1, 0], [1, 1]],
        }
    )
    doc = ProscenioDocument.model_validate(payload)
    assert isinstance(doc.sprites[0], PolygonSprite)
    assert doc.sprites[0].type == "polygon"


def test_polygon_sprite_with_explicit_type() -> None:
    payload = _doc_with_sprite(
        {
            "type": "polygon",
            "name": "arm",
            "texture_region": [0, 0, 1, 1],
            "polygon": [[0, 0], [1, 0], [1, 1]],
            "uv": [[0, 0], [1, 0], [1, 1]],
        }
    )
    doc = ProscenioDocument.model_validate(payload)
    assert isinstance(doc.sprites[0], PolygonSprite)


def test_sprite_frame_branch_parses() -> None:
    payload = _doc_with_sprite(
        {
            "type": "sprite_frame",
            "name": "blink",
            "bone": "head",
            "hframes": 4,
            "vframes": 1,
            "frame": 0,
        }
    )
    doc = ProscenioDocument.model_validate(payload)
    sprite = doc.sprites[0]
    assert isinstance(sprite, SpriteFrameSprite)
    assert sprite.hframes == 4


def test_unknown_discriminator_value_rejected() -> None:
    payload = _doc_with_sprite(
        {
            "type": "unknown_variant",
            "name": "x",
            "texture_region": [0, 0, 1, 1],
            "polygon": [[0, 0], [1, 0], [1, 1]],
            "uv": [[0, 0], [1, 0], [1, 1]],
        }
    )
    with pytest.raises(ValidationError):
        ProscenioDocument.model_validate(payload)


def test_sprite_frame_missing_required_fields_rejected() -> None:
    """``sprite_frame`` requires bone + hframes + vframes."""
    payload = _doc_with_sprite(
        {
            "type": "sprite_frame",
            "name": "blink",
        }
    )
    with pytest.raises(ValidationError):
        ProscenioDocument.model_validate(payload)


def test_generated_schema_carries_both_sprite_variants() -> None:
    """Pydantic emits both variants somewhere in the schema.

    The schema may inline them under ``properties.sprites.items`` or
    reference them through ``$defs``. Either is acceptable so long as
    both variants surface, which is what the TS / GDScript emitters
    need to walk in SPEC 014 P3 / P4.
    """
    schema = build_proscenio_schema()
    text = repr(schema)
    assert "polygon" in text
    assert "sprite_frame" in text
