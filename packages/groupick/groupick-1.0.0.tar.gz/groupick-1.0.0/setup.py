# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['groupick']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "win32"': ['windows-curses>=2.2.0,<3.0.0']}

setup_kwargs = {
    'name': 'groupick',
    'version': '1.0.0',
    'description': "Assign options to groups in the terminal with a simple GUI. Based on wong2's pick",
    'long_description': '# groupick\n\n[![image](https://github.com/anafvana/groupick/actions/workflows/ci.yml/badge.svg)](https://github.com/anafvana/groupick/actions/workflows/ci.yml)\n[![PyPI](https://img.shields.io/pypi/v/groupick.svg)](https://pypi.org/project/groupick/)\n[![PyPI](https://img.shields.io/pypi/dm/groupick)](https://pypi.org/project/groupick/)\n\n**groupick** is a small python library based on [wong2\'s pick](https://github.com/wong2/pick) which allows you to create a curses-based interactive selection in the terminal. With **groupick** you can assign options to groups.\n\n![](example/basic.gif)\n\n## Installation\n\n    $ pip install groupick\n\n## Usage\n\n**groupick** comes with a simple api:\n\n    >>> from groupick import groupick\n\n    >>> instructions = "Assign languages to groups \'a\', \'b\' or \'1\'."\n    >>> options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]\n    >>> groups:set = {"a", "b", 1}\n    >>> selected = groupick(options, groups, instructions, indicator="=>", default_index=2)\n    >>> print(f"Here is your assignment: {selected}")\n\n**output**:\n\n    >>> {\'1\': [], \'a\': [("JavaScript", 1)], \'b\': []}\n\n## Options\n\n- `options`: a list of options to choose from\n- `groups`: a list of ints and/or characters symbolising groups (max-length per item is 1)\n- `instructions`: (optional) a title above options list\n- `indicator`: (optional) custom the selection indicator, defaults to `*`\n- `default_index`: (optional) index of item where cursor starts at by default\n- `handle_all`: (optional) define whether it is mandatory to assign all options to groups, defaults to `False`\n\n## Community Projects\n\n[wong2\'s pick](https://github.com/wong2/pick): Original pick project, for selecting one or more options (no grouping)\n\n[pickpack](https://github.com/anafvana/pickpack): A fork of `groupick` to select tree data.\n',
    'author': 'Ana',
    'author_email': 'anafvana@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/anafvana/groupick/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
