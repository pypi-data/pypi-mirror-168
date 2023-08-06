# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_notes']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fn = file_notes.main:main']}

setup_kwargs = {
    'name': 'file-notes',
    'version': '0.0.2.dev0',
    'description': 'file-notes can add note information to the file. It works with Python 3.6+.',
    'long_description': "## file-notes\nfile-notes can add note information to the file. It works with Python 3.6+.\n\n## Installation\n```\npip install file-notes\n```\n\n## Usage\nCommand\n```\nfn [-l|-al|-a|-u|-d] [file_or_dir] [note]\n```\nShow all file information\n```\nfn -l\n```\nShow all file information including hidden files\n```\nfn -al\n```\nAdd a note to a file\n```\nfn -a file_or_dir_name 'note'\n```\nUpdate a file's note\n```\nfn -u file_or_dir_name 'new note'\n```\nDelete a file's note\n```\nfn -d file_or_dir_name\n```",
    'author': 'Flyer-Jia',
    'author_email': 'flyerjia@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flyerjia/file-notes',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
