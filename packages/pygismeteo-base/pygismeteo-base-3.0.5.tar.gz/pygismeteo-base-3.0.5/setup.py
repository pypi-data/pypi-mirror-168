# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygismeteo_base', 'pygismeteo_base.models', 'pygismeteo_base.periods']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9,<2.0', 'typing-extensions>=3.7.4.3,<5']

setup_kwargs = {
    'name': 'pygismeteo-base',
    'version': '3.0.5',
    'description': 'Base for pygismeteo and aiopygismeteo',
    'long_description': '# pygismeteo-base\n\n[![CI](https://github.com/monosans/pygismeteo-base/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/monosans/pygismeteo-base/actions/workflows/ci.yml)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/monosans/pygismeteo-base/main.svg)](https://results.pre-commit.ci/latest/github/monosans/pygismeteo-base/main)\n\nБаза для [pygismeteo](https://github.com/monosans/pygismeteo) и [aiopygismeteo](https://github.com/monosans/aiopygismeteo).\n\n## License / Лицензия\n\n[MIT](https://github.com/monosans/pygismeteo-base/blob/main/LICENSE)\n',
    'author': 'monosans',
    'author_email': 'hsyqixco@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monosans/pygismeteo-base',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
