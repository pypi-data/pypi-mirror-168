from importlib.metadata import entry_points

from marshmallow import Schema, fields

from ..schemas import ConfigSchema

# Call this once for performance reasons
AVAILABLE_ENTRY_POINTS = entry_points()


def get_entry_point_extensions():
    return {ep.name: ep.load() for ep in AVAILABLE_ENTRY_POINTS.get("maxbot_extensions", [])}


class ExtensionsSchema(ConfigSchema):
    @classmethod
    def from_classes(cls, extensions):
        return cls.from_dict(
            {n: fields.Nested(getattr(c, "ConfigSchema", Schema)) for n, c in extensions.items()}
        )
