# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kilroy_face_discord', 'kilroy_face_discord.resources']

package_data = \
{'': ['*']}

install_requires = \
['aiostream>=0.4,<0.5',
 'hikari==2.0.0.dev109',
 'kilroy-face-server-py-sdk>=0.7,<0.8',
 'omegaconf>=2.2,<3.0',
 'platformdirs>=2.5,<3.0',
 'pydantic[dotenv]>=1.10,<2.0',
 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['kilroy-face-discord = kilroy_face_discord.__main__:cli']}

setup_kwargs = {
    'name': 'kilroy-face-discord',
    'version': '0.5.2',
    'description': 'kilroy face for Discord 🎮',
    'long_description': '<h1 align="center">kilroy-face-discord</h1>\n\n<div align="center">\n\nkilroy face for Discord 🎮\n\n[![Lint](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/lint.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/lint.yaml)\n[![Multiplatform tests](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/test-multiplatform.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/test-multiplatform.yaml)\n[![Docker tests](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/test-docker.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/test-docker.yaml)\n[![Docs](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/docs.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-discord/actions/workflows/docs.yaml)\n\n</div>\n\n---\n\n## Installing\n\nUsing `pip`:\n\n```sh\npip install kilroy-face-discord\n```\n',
    'author': 'kilroy',
    'author_email': 'kilroymail@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kilroybot/kilroy-face-discord',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
