# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ankisiyuan', 'ankisiyuan.notetypes', 'ankisiyuan.parser']

package_data = \
{'': ['*']}

install_requires = \
['AnkiIn>=0.1.7,<0.2.0', 'siyuanhelper>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'ankisiyuan',
    'version': '0.1.0',
    'description': 'Sync Anki with Siyuan',
    'long_description': 'None',
    'author': 'clouder',
    'author_email': 'clouder0@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
