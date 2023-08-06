from dataclasses import dataclass
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel

from zenconfig.base import BaseConfig, Schema

C = TypeVar("C", bound=BaseModel)


@dataclass
class PydanticSchema(Schema[BaseModel]):
    exclude_unset: bool = False
    exclude_defaults: bool = True

    @classmethod
    def handles(cls, config_class: type) -> bool:
        return issubclass(config_class, BaseModel)

    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return cls.parse_obj(cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        return config.dict(
            exclude_unset=self.exclude_unset,
            exclude_defaults=self.exclude_defaults,
        )


BaseConfig.register_schema(PydanticSchema)
