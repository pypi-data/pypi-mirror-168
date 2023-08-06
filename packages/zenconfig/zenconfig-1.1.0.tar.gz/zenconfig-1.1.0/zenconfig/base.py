import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Dict, Generic, List, Type, TypeVar, Union


class Format(ABC):
    @classmethod
    @abstractmethod
    def handles(cls, path: Path) -> bool:
        """Return whether the format handles the extension."""

    @abstractmethod
    def load(self, path: Path) -> Dict[str, Any]:
        """Load the configuration file into a dict."""

    @abstractmethod
    def dump(self, path: Path, config: Dict[str, Any]) -> None:
        """Dump in the configuration file."""


C = TypeVar("C")


class Schema(ABC, Generic[C]):
    @classmethod
    @abstractmethod
    def handles(cls, config_class: type) -> bool:
        """Return whether the schema handles the config."""

    @abstractmethod
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        """Load the schema based on a dict configuration."""

    @abstractmethod
    def to_dict(self, config: Any) -> Dict[str, Any]:
        """Dump the config to dict."""


class BaseConfig(ABC):
    ENV_PATH: ClassVar[str] = "CONFIG"
    PATH: ClassVar[Union[str, None]] = None
    _PATH: ClassVar[Union[Path, None]] = None

    FORMATS: ClassVar[List[Type[Format]]] = []
    FORMAT: ClassVar[Union[Format, None]] = None

    SCHEMAS: ClassVar[List[Type[Schema]]] = []
    SCHEMA: ClassVar[Union[Schema, None]] = None

    @classmethod
    def register_format(cls, format_class: Type[Format]) -> None:
        cls.FORMATS.append(format_class)

    @classmethod
    def register_schema(cls, schema_class: Type[Schema]) -> None:
        cls.SCHEMAS.append(schema_class)

    @classmethod
    def _path(cls) -> Path:
        if cls._PATH:
            return cls._PATH
        found_path: Union[str, None] = None
        if cls.ENV_PATH:
            found_path = os.environ.get(cls.ENV_PATH)
        if not found_path:
            found_path = cls.PATH
        if not found_path:
            raise ValueError(
                f"could not find the config path for config {cls.__qualname__}, tried env variable {cls.ENV_PATH}"
            )
        cls._PATH = Path(found_path).expanduser().absolute()
        return cls._PATH

    @classmethod
    def _format(cls) -> Format:
        if cls.FORMAT:
            return cls.FORMAT
        ext = cls._path().suffix
        path = cls._path()
        for format_class in cls.FORMATS:
            if not format_class.handles(path):
                continue
            cls.FORMAT = format_class()
            return cls.FORMAT
        raise ValueError(
            f"unsupported config file extension {ext} for config {cls.__qualname__}, maybe you are missing an extra"
        )

    @classmethod
    def _schema(cls) -> Schema:
        if cls.SCHEMA:
            return cls.SCHEMA
        for schema_class in cls.SCHEMAS:
            if not schema_class.handles(cls):
                continue
            cls.SCHEMA = schema_class()
            return cls.SCHEMA
        raise ValueError(
            f"could not infer config schema for config {cls.__qualname__}, maybe you are missing an extra"
        )
