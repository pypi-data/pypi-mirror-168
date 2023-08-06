from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attrs

from zenconfig.base import BaseConfig, Schema
from zenconfig.encoder import Encoder

AttrsInstance: Any
if TYPE_CHECKING:
    from attr import AttrsInstance
else:
    AttrsInstance = Any

C = TypeVar("C", bound=AttrsInstance)


class AttrsSchema(Schema[C]):
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return _load_nested(cls, cfg)

    def to_dict(self, config: C, encoder: Encoder) -> Dict[str, Any]:
        return encoder(attrs.asdict(config))


BaseConfig.register_schema(AttrsSchema(), attrs.has)


def _load_nested(cls: Type[C], cfg: Dict[str, Any]) -> C:
    """Load nested attrs."""
    kwargs: Dict[str, Any] = {}
    for field in attrs.fields(cls):
        if field.name not in cfg:
            continue
        value = cfg[field.name]
        if attrs.has(field.type):
            value = _load_nested(field.type, value)
        kwargs[field.name] = value
    return cls(**kwargs)
