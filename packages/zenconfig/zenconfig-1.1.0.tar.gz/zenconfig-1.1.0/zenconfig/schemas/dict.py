from typing import Any, Dict, Type, TypeVar

from zenconfig.base import BaseConfig, Schema

C = TypeVar("C", bound=dict)


class DictSchema(Schema[C]):
    @classmethod
    def handles(cls, config_class: type) -> bool:
        return issubclass(config_class, dict)

    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return cls(cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        return dict(config)


BaseConfig.register_schema(DictSchema)
