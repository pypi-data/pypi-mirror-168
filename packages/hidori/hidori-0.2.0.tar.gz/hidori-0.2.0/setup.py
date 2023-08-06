# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'hidori_cli': 'src/hidori_cli',
 'hidori_cli.apps': 'src/hidori_cli/apps',
 'hidori_cli.commands': 'src/hidori_cli/commands',
 'hidori_core': 'src/hidori_core',
 'hidori_core.compat': 'src/hidori_core/compat',
 'hidori_core.modules': 'src/hidori_core/modules',
 'hidori_core.schema': 'src/hidori_core/schema',
 'hidori_core.utils': 'src/hidori_core/utils',
 'hidori_pipelines': 'src/hidori_pipelines',
 'hidori_runner': 'src/hidori_runner',
 'hidori_runner.drivers': 'src/hidori_runner/drivers',
 'hidori_runner.executors': 'src/hidori_runner/executors',
 'hidori_runner.transports': 'src/hidori_runner/transports'}

packages = \
['hidori_cli',
 'hidori_cli.apps',
 'hidori_cli.commands',
 'hidori_common',
 'hidori_core',
 'hidori_core.compat',
 'hidori_core.modules',
 'hidori_core.schema',
 'hidori_core.utils',
 'hidori_pipelines',
 'hidori_runner',
 'hidori_runner.drivers',
 'hidori_runner.executors',
 'hidori_runner.transports']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.3.0,<5.0.0']

entry_points = \
{'console_scripts': ['hidori-pipeline = hidori_cli.apps.pipeline:main']}

setup_kwargs = {
    'name': 'hidori',
    'version': '0.2.0',
    'description': 'A modern, agentless, zero-dependency system state assurance',
    'long_description': '# Hidori\n\n[![PyPI](https://img.shields.io/pypi/v/hidori)](https://pypi.org/project/hidori/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/hidori-dev/hidori/main.svg)](https://results.pre-commit.ci/latest/github/hidori-dev/hidori/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/hidori-dev/hidori)\n\nHidori is a modern, agentless, zero-dependency[^1][^2] variation on updating system state. General rule of thumb is that changes to the system are only done if the requested state is different from the actual state. Hidori modules are idempotent if the system is already in the desired state.\nEvery change in the target system is reported through the modules log as "affected".\n\nHidori communicates with a target machine through appropriate protocol that is designated by the chosen driver.\n\n## Install\n\nDepending on your environment you might wish to install Hidori globally or locally using chosen Python dependency manager such as poetry or pip.\nUltimately, the choice is yours. Either way, Hidori is safe for your Python environment - it does not pull any dependencies from PyPI[^2].\n\nExample using pip:\n```sh\npip install hidori\n```\n\n## Hello World\n\nWith Hidori installed you need a single TOML file that provides where and what should be done. A simple \'hello world\' example assuming that some machine is available at the given IP address:\n\n```toml\n[hosts]\n\n  [hosts.vm]\n  ip = "192.168.122.31"\n  user = "root"\n\n[tasks]\n\n  [tasks."Say hello"]\n  module = "hello"\n```\n\nNow you just need to run it (example assumes the file is named `pipeline.toml`):\n\n```sh\nhidori-pipeline run pipeline.toml\n```\n\nThe result on my machine is:\n\n```\n[root@vm: Say hello]\n[16:03:19] OK: Hello from Linux debian 4.19.0-21-amd64\n```\n\n## Support\n\nIn general, Hidori is based on Python 3.11, but `hidori_core` runs with any version of Python that is still supported.\nReason for that is vast majority of target systems don\'t have the latest Python runtime installed, so therefore `hidori_core`\nwhich includes all the code that runs on a target system can be expected to be supported according to the following table:\n\n| Python Version |     EOL Date     |\n| -------------- | ---------------- |\n| 3.7            | July 2023        |\n| 3.8            | November 2024    |\n| 3.9            | November 2025    |\n| 3.10           | November 2026    |\n| 3.11           | November 2027(?) |\n\n## Development\n\nThe dev environment can be setup with poetry:\n```sh\npoetry install\n```\n\n[^1]: Except for the necessary runtime - python, and system libraries that are used by modules\n[^2]: typing-extensions are necessary until at least July 2023 when Python 3.7\'s support will end\n\n## License\n\nHidori is licensed under both the [MIT](LICENSE-MIT) and the [EUPL-1.2](LICENSE-EUPL) licenses.\n',
    'author': 'Piotr Szpetkowski',
    'author_email': 'piotr.szpetkowski@pyquest.space',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hidori-dev/hidori',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
