import sys
from abc import ABC
from typing import ClassVar, Dict

from zenconfig.read import ReadOnlyConfig


class Config(ReadOnlyConfig, ABC):
    FILE_MODE: ClassVar[int] = 0o600

    def save(self) -> None:
        """Save the current config to the file."""
        if not self._path().exists():
            self._path().touch(mode=self.FILE_MODE)
        self._format().dump(self._path(), self._schema().to_dict(self))

    def clear(self) -> None:
        """Remove the config file."""
        kwargs: Dict[str, bool] = {}
        if sys.version_info[:2] != (3, 7):
            kwargs["missing_ok"] = True
        self._path().unlink(**kwargs)
