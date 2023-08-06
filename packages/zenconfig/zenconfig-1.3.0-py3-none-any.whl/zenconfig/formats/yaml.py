from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import yaml

from zenconfig.base import BaseConfig, Format


@dataclass
class YAMLFormat(Format):
    indent: int = 2
    sort_keys: bool = True

    def load(self, path: Path) -> Dict[str, Any]:
        return yaml.safe_load(path.read_text())

    def dump(
        self,
        path: Path,
        config: Dict[str, Any],
        encoder: Optional[Callable[[Any], Any]],
    ) -> None:
        path.write_text(
            yaml.safe_dump(config, indent=self.indent, sort_keys=self.sort_keys)
        )


BaseConfig.register_format(YAMLFormat(), ".yaml", ".yml")
