# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_tracker', 'time_tracker.tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<2.0.0', 'appdirs>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['trt = time_tracker.__main__:main']}

setup_kwargs = {
    'name': 'tiempo-tracker',
    'version': '0.1.1',
    'description': 'Easy to use CLI time tracker written in Python',
    'long_description': ".. image:: https://api.codeclimate.com/v1/badges/bd649a97a34c7f8c4634/maintainability\n   :target: https://codeclimate.com/github/dmikhr/tiempo-tracker/maintainability\n   :alt: Maintainability\n\nIntroduction\n=========================\nTrack time you've spent on different tasks. Then see how much time you've spent on each. \n\nContinuation of `time_management <https://github.com/dmikhr/time_management>`_ script idea.\n\n\n**Development**\n=========================\nBuilt with Python, Poetry, SQLAlchemy for managing database, SQLite as database. \n\nTesting: Pytest\n\nRun package without building: ``poetry run python -m time_tracker [options]`` in the project directory\n\nExample: ``poetry run python -m time_tracker -a Task1``\n\nRun tests: ``poetry run pytest``\n\n\n**Installation**\n=========================\n**From source**\n\nrun ``make build`` and then ``make package-install`` in the package directory.\n\n**PIP**\n\nrun ``pip install tiempo-tracker``\n\nWhen you run app for the first time it will create a database. You'll see a message:\n\n``Database not found. Creating new one``\n\nAlso app will show path where database is stored.\n\n\n**Usage**\n=========================\ntiempo-tracker can be invoked by ``trt`` command in the terminal.\nAvailable options:\n::\n\n    -h, --help            show this help message and exit\n    -s START, --start START\n                            Start task by providing its name\n    -f, --finish          Finish current task. Task also can be finished \n                            by starting a different task\n    -a ADD, --add ADD     Add new task\n    -r REMOVE, --remove REMOVE\n                            Remove the task\n    -l, --list            List of all tasks\n    -st STATS, --stats STATS\n                            Stats about tasks\n\n\nStart with adding new task:\n\n``trt -a task1``\n\nThen track the task:\n\n``trt -s task1``\n\nTo finish the task either start a new one (add new task first if it doesn't exist yet):\n\n``trt -s task2``\n\nor finish task\n\n``trt -f``\n\nShow all added tasks:\n\n``trt -l``\n\nIf particular task is in progress there will be ``(in progress)`` status near this task. Example:\n::\n\n    Project_work\n    Exercising (in progress)\n    Flask_API_project\n    Some_task\n\nRemove task if it's no longer needed:\n\n``trt -r task1``\n\nSee how much time you've spent on each task during the day:\n\n``trt -st``\n\nTime will be presented in two formats: ``hr:min`` and as a decimal number. The latter is convenient for further storage in spreadsheets.",
    'author': 'Dmitrii Khramtsov',
    'author_email': 'dmitrypkh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmikhr/tiempo-tracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
