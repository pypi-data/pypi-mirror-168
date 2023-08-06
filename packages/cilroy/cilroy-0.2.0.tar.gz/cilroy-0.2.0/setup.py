# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cilroy',
 'cilroy.controller',
 'cilroy.posting',
 'cilroy.resources',
 'cilroy.scoring']

package_data = \
{'': ['*']}

install_requires = \
['aiostream>=0.4,<0.5',
 'betterproto>=2.0.0b5,<3.0.0',
 'jsonschema>=4.7,<5.0',
 'kilroy-face-client-py-sdk>=0.6,<0.7',
 'kilroy-module-client-py-sdk>=0.7,<0.8',
 'kilroy-server-py-utils>=0.3,<0.4',
 'omegaconf>=2.2,<3.0',
 'platformdirs>=2.5,<3.0',
 'pydantic[dotenv]>=1.10,<2.0',
 'pyhumps>=3.7,<4.0',
 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['cilroy = cilroy.__main__:cli']}

setup_kwargs = {
    'name': 'cilroy',
    'version': '0.2.0',
    'description': 'kilroy controller 🎛️',
    'long_description': '<h1 align="center">cilroy</h1>\n\n<div align="center">\n\nkilroy controller 🎛️\n\n[![Lint](https://github.com/kilroybot/cilroy/actions/workflows/lint.yaml/badge.svg)](https://github.com/kilroybot/cilroy/actions/workflows/lint.yaml)\n[![Multiplatform tests](https://github.com/kilroybot/cilroy/actions/workflows/test-multiplatform.yaml/badge.svg)](https://github.com/kilroybot/cilroy/actions/workflows/test-multiplatform.yaml)\n[![Docker tests](https://github.com/kilroybot/cilroy/actions/workflows/test-docker.yaml/badge.svg)](https://github.com/kilroybot/cilroy/actions/workflows/test-docker.yaml)\n[![Docs](https://github.com/kilroybot/cilroy/actions/workflows/docs.yaml/badge.svg)](https://github.com/kilroybot/cilroy/actions/workflows/docs.yaml)\n\n</div>\n\n---\n\nTODO\n',
    'author': 'kilroy',
    'author_email': 'kilroymail@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kilroybot/cilroy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
