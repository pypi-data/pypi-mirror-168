import sys
from abc import ABC
from typing import ClassVar, Dict

from zenconfig.base import ZenConfigError
from zenconfig.read import ReadOnlyConfig


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
            path.touch(mode=self.FILE_MODE)
        self._format().dump(path, self._schema().to_dict(self))

    def clear(self) -> None:
        """Delete the config file(s)."""
        kwargs: Dict[str, bool] = {}
        if sys.version_info[:2] != (3, 7):
            kwargs["missing_ok"] = True
        for path in self._paths():
            path.unlink(**kwargs)
