# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evola', 'evola.epso']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.0,<4.0.0', 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'evola',
    'version': '0.0.3',
    'description': 'Evolutionary algorithms',
    'long_description': '# Evolutionary algorithms in Python\n\nThere are three algorithms implemented in this package (from best to worse):\n\n- epso (Evolutionary Particle Swarm Optimization)\n- pso (Particle Swarm Optimization) (tbd)\n- pop (Classic Genetic Algorithm) (tbd)\n',
    'author': 'David Freire',
    'author_email': 'up201806711@up.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DavidFreire-FEUP/evolutionary-algorithms',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
