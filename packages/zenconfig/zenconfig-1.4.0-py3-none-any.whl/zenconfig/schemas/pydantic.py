import contextlib
from dataclasses import dataclass
from functools import partial
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel

from zenconfig.base import BaseConfig, Schema
from zenconfig.encoder import Encoder, encode

C = TypeVar("C", bound=BaseModel)


@dataclass
class PydanticSchema(Schema[C]):
    exclude_unset: bool = False
    exclude_defaults: bool = True

    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return cls.parse_obj(cfg)

    def to_dict(self, config: C, encoder: Encoder) -> Dict[str, Any]:
        # Use pydantic encoders.
        return _encoder(config)(
            config.dict(
                exclude_unset=self.exclude_unset,
                exclude_defaults=self.exclude_defaults,
            )
        )


BaseConfig.register_schema(PydanticSchema(), lambda cls: issubclass(cls, BaseModel))


def _encoder(config: BaseModel) -> Encoder:
    def _enc(obj: Any) -> Any:
        with contextlib.suppress(TypeError):
            return config.__json_encoder__(obj)  # type: ignore
        return obj

    return partial(encode, _enc)
