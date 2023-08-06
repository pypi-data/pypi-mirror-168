# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['d3_scripts']

package_data = \
{'': ['*'], 'd3_scripts': ['schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bidict>=0.22.0,<0.23.0',
 'ipython>=8.4.0,<9.0.0',
 'iteration-utilities>=0.11.0,<0.12.0',
 'jsonschema>=4.4.0,<5.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'networkx>=2.8.3,<3.0.0',
 'pandas>=1.4.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'yamllint>=1.26.3,<2.0.0']

entry_points = \
{'console_scripts': ['d3-cli = d3_scripts.d3_cli:cli']}

setup_kwargs = {
    'name': 'd3-cli',
    'version': '0.1.4',
    'description': 'Utility scripts for ManySecured-D3 claims',
    'long_description': '# ManySecured d3-cli\n\nUtility cli for ManySecured-D3 claims\n\n## Installation\n\nThis api may be installed using pip like so:\n\n```\npip install d3-cli\n```\n\nWhen developing these scripts, [Python Poetry](https://python-poetry.org/)\nis used to install and manage dependencies as well as publish to [PyPI](https://pypi.org/).\n\nPoetry will create a python isolated virtual environment in the `./.venv` folder and install dependencies if you run:\n\n```bash\npoetry install\n```\n\nYou cannot run the cli or scripts directly from the `./src/d3-scripts` since we are using [Python relative imports](https://realpython.com/absolute-vs-relative-python-imports/#relative-imports).\n\nInstead, you must run the d3-cli script defined in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./pyproject.toml):\n\n## Usage\n\n```console\nusage: d3-cli [-h] [--version] [--guid] [--output [OUTPUT]]\n              [--mode [{build,lint,export}]] [--build-dir [BUILD_DIR]]\n              [--check_uri_resolves] [--verbose | --quiet]\n              [input ...]\n\nManySecured D3 CLI for creating, linting and exporting D3 claims\n\npositional arguments:\n  input                 Folders containing D3 YAML files. (default: [])\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             Show the version and exit. (default: False)\n  --guid, --uuid        Generate and show guid and exit. (default:\n                        False)\n  --output [OUTPUT]     Directory in which to output built claims.\n                        (default: <cwd>/d3-build)\n  --mode [{build,lint,export}], -m [{build,lint,export}]\n                        Mode to run d3-cli in. (default: build)\n  --build-dir [BUILD_DIR]\n                        Build directory with json claims to export.\n                        Specifying this will skip build step in export\n                        mode. (default: None)\n  --check_uri_resolves  Check that URIs/refs resolve. This can be very\n                        slow, so you may want to leave this off\n                        normally. (default: False)\n  --verbose, -v\n  --quiet, -q\n\nExample: d3-cli ./manufacturers\n```\n\n## Tests\n\nTests can be run via:\n\n```bash\npoetry run pytest\n```\n\n## Publish\n\nThe d3-cli utility is published [here](https://pypi.org/project/d3-cli/).\n\nIn order to publish you must run:\n\n```\npoetry build\npoetry publish\n```\n\nAnd then enter the credentials for the NquiringMinds pypi account.\n',
    'author': 'NquiringMinds',
    'author_email': 'contact@nquiringminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TechWorksHub/ManySecured-D3DB',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
