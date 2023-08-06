from abc import ABC
from typing import Type, TypeVar

from zenconfig.base import BaseConfig

C = TypeVar("C", bound="ReadOnlyConfig")


class ReadOnlyConfig(BaseConfig, ABC):
    @classmethod
    def load(cls: Type[C]) -> C:
        return cls._schema().from_dict(cls, cls._format().load(cls._path()))
