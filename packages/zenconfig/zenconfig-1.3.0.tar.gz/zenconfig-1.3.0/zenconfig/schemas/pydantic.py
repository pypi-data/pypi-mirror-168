from dataclasses import dataclass
from typing import Any, Callable, Dict, Type, TypeVar

from pydantic import BaseModel

from zenconfig.base import BaseConfig, Schema

C = TypeVar("C", bound=BaseModel)


@dataclass
class PydanticSchema(Schema[C]):
    exclude_unset: bool = False
    exclude_defaults: bool = True

    def encoder(self, config: C) -> Callable[[Any], Any]:
        """Use the class custom encoder."""
        return config.__json_encoder__  # type: ignore

    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return cls.parse_obj(cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        return config.dict(
            exclude_unset=self.exclude_unset,
            exclude_defaults=self.exclude_defaults,
        )


BaseConfig.register_schema(PydanticSchema(), lambda cls: issubclass(cls, BaseModel))
