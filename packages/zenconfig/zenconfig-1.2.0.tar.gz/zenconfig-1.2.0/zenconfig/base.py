import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)


class ZenConfigError(Exception):
    """Default error when Handling config files."""


class Format(ABC):
    """Abstract class for handling different file formats."""

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
    """Abstract class for handling different config class types."""

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
    """Abstract base class for handling config files."""

    # Environment variable name holding the config file path to load.
    ENV_PATH: ClassVar[str] = "CONFIG"
    # Hardcoded config file path to load.
    # Fallback when no path is found in the environment variable.
    PATH: ClassVar[Optional[str]] = None
    # Paths of all config files handled.
    _PATHS: ClassVar[Optional[Tuple[Path, ...]]] = None

    # All format classes supported.
    FORMATS: ClassVar[List[Type[Format]]] = []
    # Selected format class instance.
    FORMAT: ClassVar[Optional[Format]] = None

    # All schema classes supported.
    SCHEMAS: ClassVar[List[Type[Schema]]] = []
    # Selected schema class instance.
    SCHEMA: ClassVar[Optional[Schema]] = None

    @classmethod
    def register_format(cls, format_class: Type[Format]) -> None:
        """Add a format class to the list of supported ones."""
        cls.FORMATS.append(format_class)

    @classmethod
    def register_schema(cls, schema_class: Type[Schema]) -> None:
        """Add a schema class to the list of supported ones."""
        cls.SCHEMAS.append(schema_class)

    @classmethod
    def _paths(cls) -> Tuple[Path, ...]:
        """Cached method to get all handled file paths."""
        if cls._PATHS:
            return cls._PATHS
        found_path: Optional[str] = None
        if cls.ENV_PATH:
            found_path = os.environ.get(cls.ENV_PATH)
        if not found_path:
            found_path = cls.PATH
        if not found_path:
            raise ZenConfigError(
                f"could not find the config path for config {cls.__qualname__}, tried env variable {cls.ENV_PATH}"
            )
        cls._PATHS = tuple(
            sorted(_handle_globbing(Path(found_path).expanduser().absolute()))
        )
        return cls._PATHS

    @classmethod
    def _format(cls, path: Optional[Path] = None) -> Format:
        """Get the format instance for a path."""
        if cls.FORMAT:
            return cls.FORMAT
        if path:
            _path = path
        else:
            paths = cls._paths()
            if len(paths) != 1:
                raise ZenConfigError(
                    "multiple configuration files, use the path parameter"
                )
            _path = paths[0]
        for format_class in cls.FORMATS:
            if not format_class.handles(_path):
                continue
            fmt = format_class()
            if not path:
                cls.FORMAT = fmt
            return fmt
        raise ZenConfigError(
            f"unsupported config file {path.name} for config {cls.__qualname__}, maybe you are missing an extra"  # type: ignore
        )

    @classmethod
    def _schema(cls) -> Schema:
        """Get the schema instance for this config class."""
        if cls.SCHEMA:
            return cls.SCHEMA
        for schema_class in cls.SCHEMAS:
            if not schema_class.handles(cls):
                continue
            cls.SCHEMA = schema_class()
            return cls.SCHEMA
        raise ZenConfigError(
            f"could not infer config schema for config {cls.__qualname__}, maybe you are missing an extra"
        )


def _handle_globbing(original_path: Path) -> Iterator[Path]:
    """Convert a glob path to all matched paths."""
    directory = Path(original_path)
    glob = False
    while "*" in directory.name or "?" in directory.name or "[" in directory.name:
        directory = directory.parent
        glob = True
    if not glob:
        yield original_path
    else:
        for path in directory.rglob(str(original_path.relative_to(directory))):
            if path.is_file():
                yield path
