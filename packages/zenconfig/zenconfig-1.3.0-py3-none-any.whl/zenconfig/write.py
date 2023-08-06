import logging
import sys
from abc import ABC
from typing import ClassVar, Dict

from zenconfig.base import ZenConfigError
from zenconfig.read import ReadOnlyConfig

logger = logging.getLogger(__name__)


class Config(ReadOnlyConfig, ABC):
    """Abstract base class for handling read and write operations."""

    # File mode used if we need to create the config file.
    FILE_MODE: ClassVar[int] = 0o600

    def save(self) -> None:
        """Save the current config to the file."""
        paths = self._paths()
        if len(paths) != 1:
            raise ZenConfigError(
                "cannot save when handling multiple configuration files"
            )
        path = paths[0]
        if not path.exists():
            logger.debug("creating file at path %s", path)
            path.touch(mode=self.FILE_MODE)
        fmt = self._format()
        logger.debug(
            "using %s to save %s to %s",
            fmt.__class__.__name__,
            self.__class__.__name__,
            path,
        )
        schema = self._schema()
        fmt.dump(path, schema.to_dict(self), schema.encoder(self))

    def clear(self) -> None:
        """Delete the config file(s)."""
        kwargs: Dict[str, bool] = {}
        if sys.version_info[:2] != (3, 7):
            kwargs["missing_ok"] = True
        for path in self._paths():
            logger.debug("deleting file at path %s", path)
            path.unlink(**kwargs)
