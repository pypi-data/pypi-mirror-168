# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_projetaai',
 'kedro_projetaai.cli',
 'kedro_projetaai.packing',
 'kedro_projetaai.serving',
 'kedro_projetaai.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Cors>=3.0.10,<4.0.0',
 'Flask>=2.2.2,<3.0.0',
 'GitPython>=3.1.27,<4.0.0',
 'attr>=0.3.2,<0.4.0',
 'click>=8.1.3,<9.0.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'flatten-dict>=0.4.2,<0.5.0',
 'kedro>=0.18.2,<0.19.0',
 'pydantic>=1.10.2,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'waitress>=2.1.2,<3.0.0']

entry_points = \
{'kedro.hooks': ['projetaai-overrides = kedro_projetaai.plugin:overrides'],
 'kedro.project_commands': ['projetaai = kedro_projetaai.plugin:cli'],
 'kedro.starters': ['projetaai = kedro_projetaai.starters:project_starters'],
 'projetaai.cli': ['local = kedro_projetaai.cli.local:LocalCLI']}

setup_kwargs = {
    'name': 'kedro-projetaai',
    'version': '0.1.0b1',
    'description': 'Kedro plugin that adds interfaces for production',
    'long_description': '# Kedro ProjetaAi\n\n## Introduction\n\nKedro ProjetaAi is a Kedro Plugin that discretizes production patterns, and \nextends Kedro in order to enable cloud solutions into a Kedro environment.\n\n## Usable\n\n### CLI Extension\n\n`kedro_projetaai.cli.plugin.ProjetaAiCLIPlugin` provides an interface with\npredefined commands to inherit and override in order to create new integrations\nbetween ProjetaAi/Kedro and a cloud solution.\n',
    'author': 'Ipiranga',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
