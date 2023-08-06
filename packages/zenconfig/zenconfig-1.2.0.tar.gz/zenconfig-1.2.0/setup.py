# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zenconfig', 'zenconfig.formats', 'zenconfig.schemas']

package_data = \
{'': ['*']}

extras_require = \
{'pydantic': ['pydantic>=1,<2'],
 'toml': ['tomli>=2,<3', 'tomli-w>=1,<2'],
 'yaml': ['PyYAML>=6,<7']}

setup_kwargs = {
    'name': 'zenconfig',
    'version': '1.2.0',
    'description': 'Simple configuration loader for python.',
    'long_description': '# zen-config\n\n[![tests](https://github.com/gpajot/zen-config/workflows/Test/badge.svg?branch=main&event=push)](https://github.com/gpajot/zen-config/actions?query=workflow%3ATest+branch%3Amain+event%3Apush)\n[![version](https://img.shields.io/pypi/v/zenconfig?label=stable)](https://pypi.org/project/zenconfig/)\n[![python](https://img.shields.io/pypi/pyversions/zenconfig)](https://pypi.org/project/zenconfig/)\n\nSimple configuration loader for python.\n\nCompared to other solutions, the goal is to bring:\n- simple usage for simple use cases\n- multiple format support\n- use objects rather than plain dict to interact with the config\n- optionally use the power of pydantic for validation\n\n## Simple usage\nIf you don\'t want to configure much, pass the config path through the env variable `CONFIG`, and simply use:\n```python\nfrom dataclasses import dataclass\nfrom zenconfig import Config\n\n@dataclass\nclass MyConfig(Config):\n    some_key: str\n    some_optional_key: bool = False\n\n\ncfg = MyConfig(some_key="hello")\ncfg.save()\n...\ncfg = MyConfig.load()\ncfg.some_optional_key = True\ncfg.save()\n...\ncfg.clear()\n```\n\n## Config file loading\nWhen creating your config, you can specify at least one of those two attributes:\n- `ENV_PATH` the environment variable name containing the path to the config file, defaults to `CONFIG`\n- `PATH` directly the config path\n\n> 💡 When supplying both, if the env var is not set, it will use `PATH`.\n\nUser constructs will be expanded.\nIf the file does not exist it will be created (not parent directories though).\nYou can specify the file mode via `Config.FILE_MODE`.\n\nThe config can be loaded from multiple files, see [fnmatch](https://docs.python.org/3/library/fnmatch.html) for syntax.\nNote that you will not be able to save if not handling exactly one file.\n\n## Read only\nIf you do not want to be able to modify the config from your code, you can use `ReadOnlyConfig`.\n\n## Supported formats\nCurrently, those formats are supported:\n- JSON\n- YAML - requires the `yaml` extra\n- TOML - requires the `toml` extra\n\nThe format is automatically inferred from the config file extension.\nWhen loading from multiple files, files can be of multiple formats.\n\nOther formats can be added by subclassing `Format`.\n\nTo register more formats: `Config.register_format(MyFormat)`.\n\nYou can also force the format using `Config.FORMAT = MyFormat(...)`.\nThis can be used to disable auto selection, or pass parameters to the format. \n\n## Supported schemas\nCurrently, those schemas are supported:\n- plain dict\n- dataclasses\n- pydantic models - requires the `pydantic` extra\n\n\nThe schema is automatically inferred from the config class.\n\nOther schemas can be added by subclassing `Schema`.\n\nTo register more schemas: `Config.register_schema(MySchema)`.\n\nYou can also force the schema using `Config.SCHEMA = MySchema(...)`.\nThis can be used to disable auto selection, or pass parameters to the schema.\n\nTo use pydantic:\n```python\nfrom pydantic import BaseModel\nfrom zenconfig import Config\n\nclass MyPydanticConfig(Config, BaseModel):\n    ...\n```\n\n> ⚠️ When using pydantic, you have to supply the `ClassVar` type annotations\n> to all class variable you override\n> otherwise pydantic will treat those as its own fields and complain.\n\n## Contributing\nSee [contributing guide](https://github.com/gpajot/zen-config/blob/main/CONTRIBUTING.md).\n',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/zen-config',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
