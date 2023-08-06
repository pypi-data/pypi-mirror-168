# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nx3d', 'nx3d.examples']

package_data = \
{'': ['*'], 'nx3d': ['data/*']}

install_requires = \
['Panda3D>=1.10,<2.0', 'networkx>=2.8,<3.0', 'numpy>=1.23,<2.0']

setup_kwargs = {
    'name': 'nx3d',
    'version': '22.10.0',
    'description': 'The missing 3D plotting functionality for networkx',
    'long_description': '# nx3d\n\n[![-missing homepage-](https://img.shields.io/badge/home-GitHub-blueviolet)](https://github.com/ekalosak/nx3d)\n[![-missing docs-](https://img.shields.io/badge/docs-ReadTheDocs-blue)](https://nx3d.readthedocs.io/en/latest/)\n[![-missing pypi-](https://img.shields.io/pypi/v/nx3d)](https://pypi.org/project/nx3d/)\n[![-missing build status-](https://img.shields.io/github/workflow/status/ekalosak/nx3d/Build%20nx3d%20and%20publish%20to%20PyPi)](https://github.com/ekalosak/nx3d/actions)\n\n![-missing project maturity-](https://img.shields.io/badge/status-experimental-green)\n[![-missing download count-](https://img.shields.io/pypi/dw/nx3d)](https://pypistats.org/packages/nx3d)\n\nThe missing 3D plotting functionality for the excellent `networkx` Python package.\n\n![-missing gif of frucht graph-](https://raw.githubusercontent.com/ekalosak/nx3d/cf473d1dfab506ecd4044f4693c09aea0e1153ba/data/frucht.gif)\n\n# Installation\n```sh\npip install nx3d\n```\n\n## Check your installation\n\n### Basic demo\n```sh\npython -m nx3d\n```\n\n### Diffusion demo\n```sh\npython -m nx3d diffusion\n```\n\n### Game of Life demo\n```sh\npython -m nx3d life\n```\n\n# Usage\nIn your Python code:\n```python\nimport networkx as nx\nimport nx3d\n\ng = nx.frucht_graph()\nnx3d.plot(g)\n```\n\n# Next steps\nCheck out the [docs](https://nx3d.readthedocs.io/en/latest/) for tutorials, how-to-guides, explanations, and reference\nmaterial.\n',
    'author': 'Eric Kalosa-Kenyon',
    'author_email': 'helloateric@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ekalosak/nx3d',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
