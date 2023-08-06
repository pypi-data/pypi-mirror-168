from dataclasses import asdict, fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

from zenconfig.base import BaseConfig, Schema
from zenconfig.encoder import Encoder

C = TypeVar("C")


class DataclassSchema(Schema[C]):
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return _load_nested(cls, cfg)

    def to_dict(self, config: C, encoder: Encoder) -> Dict[str, Any]:
        return encoder(asdict(config))


BaseConfig.register_schema(DataclassSchema(), is_dataclass)


def _load_nested(cls: Type[C], cfg: Dict[str, Any]) -> C:
    """Load nested dataclasses."""
    kwargs: Dict[str, Any] = {}
    for field in fields(cls):
        if field.name not in cfg:
            continue
        value = cfg[field.name]
        if is_dataclass(field.type):
            value = _load_nested(field.type, value)
        kwargs[field.name] = value
    return cls(**kwargs)
