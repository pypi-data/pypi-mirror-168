# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hugit']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'attrs>=21.4.0,<22.0.0',
 'click>=8.1.0,<9.0.0',
 'datasets>=2.0.0,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'toolz>=0.11.2,<0.12.0',
 'typed-settings>=1.0.0,<2.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['hugit = hugit.cli:cli']}

setup_kwargs = {
    'name': 'hugit',
    'version': '0.0.6',
    'description': 'Hugit',
    'long_description': '# Hugit\n\n[![PyPI](https://img.shields.io/pypi/v/hugit.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/hugit.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/hugit)][python version]\n[![License](https://img.shields.io/pypi/l/hugit)][license]\n\n[![Read the documentation at https://hugit.readthedocs.io/](https://img.shields.io/readthedocs/hugit-cli/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/davanstrien/hugit-cli/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/davanstrien/hugit-cli/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/hugit/\n[status]: https://pypi.org/project/hugit/\n[python version]: https://pypi.org/project/hugit\n[license]: https://opensource.org/licenses/MIT\n[read the docs]: https://hugit-cli.readthedocs.io/\n[tests]: https://github.com/davanstrien/hugit/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/davanstrien/hugit\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n**Warning**: this code is very much a work in progress and is primarily being intended for a particular workflow. It may not work well (or at all)\xa0for your workflow.\n\n`hugit` is a command line tool for loading ImageFolder style datasets into a 🤗 `datasets` `Dataset` and pushing to the 🤗 hub.\n\nThe primary goal of `hugit` is to help quickly get a local dataset into a format that can be used for training computer vision models. `hugit` was developed to support the workflow for [`flyswot`](https://github.com/davanstrien/flyswot/) where we wanted a quicker iteration between creating new training data, training a model, and using the new model inside [`flyswot`](https://github.com/davanstrien/flyswot/).\n\n![hugit workflow diagram](/docs/assets/hugit-workflow.png)\n\n## Supported formats\n\nAt the moment **hugit** supports ImageFolder style datasets i.e:\n\n```bash\ndata/\n    dog/\n        dog1.jpg\n    cat/\n        cat.1.jpg\n\n```\n\n## Features\n\n- A command line interface for quickly loading a dataset stored on disk into a 🤗 `datasets.Dataset`\n- Push your local dataset to the 🤗 hub\n- Get statistics about your dataset. These statistics focus on \'high level\' statistic that would be useful to include in Datasheets and Model Cards. Currently these statistics include:\n  - label frequencies, organised by split\n  - train, test, valid split sizes\n\n## Installation\n\nYou can install _Hugit_ via [pip] from [PyPI], inside a virtual environment install `hugit` using\n\n```console\n$ pip install hugit\n```\n\nAlternatively, you can use [pipx](https://pypa.github.io/pipx/) to install `hugit`\n\n```console\n$ pipx install hugit\n```\n\n## Usage\n\nYou can see help for `hugit` using `hugit --help`\n\n<!-- [[[cog\nimport cog\nfrom hugit import cli\nfrom click.testing import CliRunner\nrunner = CliRunner()\nresult = runner.invoke(cli.cli, ["--help"])\nhelp = result.output.replace("Usage: cli", "Usage: hugit")\ncog.out(\n    "```\\n{}\\n```".format(help)\n)\n]]] -->\n\n```\nUsage: hugit [OPTIONS] COMMAND [ARGS]...\n\n  Hugit Command Line\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  push_image_dataset  Load an ImageFolder style dataset.\n\n```\n\n<!-- [[[end]]] -->\n\nTo load an ImageFolder style dataset onto the 🤗 Hub you can use the `push_image_dataset` command.\n\n<!-- [[[cog\nimport cog\nfrom hugit import cli\nfrom click.testing import CliRunner\nrunner = CliRunner()\nresult = runner.invoke(cli.cli, ["push_image_dataset", "--help"])\nhelp = result.output.replace("Usage: cli", "Usage: hugit")\ncog.out(\n    "```\\n{}\\n```".format(help)\n)\n]]] -->\n\n```\nUsage: hugit push_image_dataset [OPTIONS] DIRECTORY\n\n  Load an ImageFolder style dataset.\n\nOptions:\n  --repo-id TEXT                  Repo id for the Hugging Face Hub  [required]\n  --private / --no-private        Whether to keep dataset private on the Hub\n                                  [default: private]\n  --do-resize / --no-do-resize    Whether to resize images before upload\n                                  [default: do-resize]\n  --size INTEGER                  Size to resize image. This will be used on the\n                                  shortest side of the image i.e. the aspect\n                                  rato will be maintained  [default: 224]\n  --preserve-file-path / --no-preserve-file-path\n                                  preserve_orginal_file_path  [default:\n                                  preserve-file-path]\n  --help                          Show this message and exit.\n\n```\n\n<!-- [[[end]]] -->\n\nUnder the hood `hugit` uses [`typed-settings`](https://typed-settings.readthedocs.io/en/latest/index.html), which means that configuration can either be done through the command line or through a `TOML` file. See [usage] for more detailed discussion of how to use `hugit`.\n\n## Contributing\n\nIt is likely that _Hugit_ may only work for our particular workflow. With that said if you have suggestions please open an issue.\n\n## License\n\nDistributed under the terms of the [MIT license],\n_Hugit_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[cookiecutter]: https://github.com/audreyr/cookiecutter\n[mit license]: https://opensource.org/licenses/MIT\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/davanstrien/hugit/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[contributor guide]: https://github.com/davanstrien/hugit/blob/main/CONTRIBUTING.md\n[usage]: https://hugit-cli.readthedocs.io/en/latest/usage.html\n',
    'author': 'Daniel van Strien',
    'author_email': 'daniel.van-strien@bl.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davanstrien/hugit-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
