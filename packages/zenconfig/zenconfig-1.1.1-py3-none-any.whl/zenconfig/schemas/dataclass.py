from dataclasses import asdict, fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

from zenconfig.base import BaseConfig, Schema

C = TypeVar("C")


class DataclassSchema(Schema[C]):
    @classmethod
    def handles(cls, config_class: type) -> bool:
        return is_dataclass(config_class)

    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return _load_nested(cls, cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        cfg: Dict[str, Any] = {}
        for field in fields(config):
            value = getattr(config, field.name)
            if is_dataclass(field.type):
                value = asdict(value)
            cfg[field.name] = value
        return cfg


BaseConfig.register_schema(DataclassSchema)


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
