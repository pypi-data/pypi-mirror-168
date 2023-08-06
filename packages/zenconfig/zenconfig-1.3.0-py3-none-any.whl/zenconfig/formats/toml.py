from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import tomli
import tomli_w

from zenconfig.base import BaseConfig, Format


@dataclass
class TOMLFormat(Format):
    multiline_strings: bool = True

    def load(self, path: Path) -> Dict[str, Any]:
        return tomli.loads(path.read_text())

    def dump(
        self,
        path: Path,
        config: Dict[str, Any],
        encoder: Optional[Callable[[Any], Any]],
    ) -> None:
        path.write_text(
            tomli_w.dumps(
                config,
                multiline_strings=self.multiline_strings,
            )
        )


BaseConfig.register_format(TOMLFormat(), ".toml")
