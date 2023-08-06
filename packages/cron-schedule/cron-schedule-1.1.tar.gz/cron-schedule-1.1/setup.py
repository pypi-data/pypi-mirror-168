# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['schedule']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.3.7,<2.0.0']

setup_kwargs = {
    'name': 'cron-schedule',
    'version': '1.1',
    'description': '基于cron表达式的定时任务',
    'long_description': '# cron-schedule\n\n<a href="https://pypi.org/project/cron-schedule" target="_blank">\n    <img src="https://img.shields.io/pypi/v/cron-schedule.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/cron-schedule" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/cron-schedule.svg" alt="Supported Python versions">\n</a>\n\n## Installation\n\n```bash\npip install cron-schedule \n```\n\n## Usage\n\n```python\nfrom datetime import datetime\nimport time\n\nfrom schedule import schedule\n\n\ndef do_some_job():\n    print(\'do_some_job...\', datetime.now())\n\n\nschedule.add_job(do_some_job, "* * * * * 15,25")\n\nwhile True:\n    schedule.run_pending()\n    time.sleep(1)\n```\n\n```text\ndo_some_job... 2022-09-23 15:35:15.152107\ndo_some_job... 2022-09-23 15:35:25.193932\n```\n\n#### thanks\n\n- [croniter](https://github.com/kiorky/croniter)',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
