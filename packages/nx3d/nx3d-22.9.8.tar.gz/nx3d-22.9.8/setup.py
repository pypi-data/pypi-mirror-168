# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nx3d']

package_data = \
{'': ['*'], 'nx3d': ['data/*']}

install_requires = \
['Panda3D>=1.10,<2.0', 'networkx>=2.8,<3.0', 'numpy>=1.23,<2.0']

setup_kwargs = {
    'name': 'nx3d',
    'version': '22.9.8',
    'description': 'The missing 3D plotting functionality for networkx',
    'long_description': "# nx3d\n\n[![-missing homepage-](https://img.shields.io/badge/home-GitHub-blueviolet)](https://github.com/ekalosak/nx3d)\n[![-missing docs-](https://img.shields.io/badge/docs-ReadTheDocs-blue)](https://nx3d.readthedocs.io/en/latest/)\n[![-missing pypi-](https://img.shields.io/pypi/v/nx3d)](https://pypi.org/project/nx3d/)\n[![-missing build status-](https://img.shields.io/github/workflow/status/ekalosak/nx3d/Build%20nx3d%20and%20publish%20to%20PyPi)](https://github.com/ekalosak/nx3d/actions)\n\n![-missing project maturity-](https://img.shields.io/badge/status-experimental-brightgreen)\n![-missing download count-](https://img.shields.io/pypi/dw/nx3d)\n\nThe missing 3D plotting functionality for the excellent `networkx` Python package.\n\n![-missing gif of frucht graph-](https://raw.githubusercontent.com/ekalosak/nx3d/cf473d1dfab506ecd4044f4693c09aea0e1153ba/data/frucht.gif)\n\n# Installation\nIn your shell:\n```sh\npip install nx3d\n```\n\n# Quickstart\nAfter installation,\n\n## From your shell\n```sh\npython -m nx3d autolabel\n```\n\nor\n\n```sh\npython -m nx3d diffusion\n```\n\n## In your Python REPL\n```python\nimport nx3d\nnx3d.demo()\n```\n\n# Usage\nIn your Python code:\n```python\nimport networkx as nx\nimport nx3d\n\ng = nx.frucht_graph()\nnx3d.plot(g)\n```\n\n# Contribute\nThank you for considering contributing to `nx3d`.\n\nCurrently, there's no enforced testing, formatting, linting, or typechecking with CI. Let's say that's intentional to\nkeep this young project lightweight.  With that in mind, the pre-commit hooks defined in `.pre-commit-config.yaml` apply\nlinting and formatting to keep the project clean. Please use the pre-commit hooks before opening a PR.\n\n## Clone the code\n\n## Setup the development environment\n\nYou can do this as you like, though you might consider:\n1. Install `poetry`\n2. Run `poetry shell`\n3. Run `poetry install`\n4. Verify the installation by running `python -m nx3d`\n\n## Set up pre-commit\nFrom this project's root, initialize pre-commit as follows:\n\n```sh\npre-commit install\npre-commit run -a\n```\n\n## Update the docs\n1. Update the inline docstrings and/or the files in the docs/ directory.\n2. Navigate to the docs/ dir and run `make html` to preview your changes.\n3. When you cut a PR, the CI will trigger a ReadTheDocs build.\n4. When merged, the CD will publish those docs (3).\n\n### First time updating the docs\nI used `brew install python-sphinx`, see installation instructions on [www.sphinx-doc.org](https://www.sphinx-doc.org/en/master/usage/installation.html).\n\n## Hack on some code\nSee TODO.md for open tasks.\n\n## Open a PR\n\nWhen it merges, CD will push to PyPi and ReadTheDocs.\n",
    'author': 'Eric Kalosa-Kenyon',
    'author_email': 'helloateric@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ekalosak/nx3d',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
