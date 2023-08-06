# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scheduler']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.3.7,<2.0.0']

setup_kwargs = {
    'name': 'cron-schedule',
    'version': '0.1.0',
    'description': '基于cron表达式的定时任务',
    'long_description': None,
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
