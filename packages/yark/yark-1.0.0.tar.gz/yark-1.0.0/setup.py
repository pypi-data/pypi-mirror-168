# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yark']
install_requires = \
['Flask>=2.2.2,<3.0.0',
 'colorama>=0.4.5,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'yt-dlp>=2022.8.19,<2023.0.0']

entry_points = \
{'console_scripts': ['yark = yark:main']}

setup_kwargs = {
    'name': 'yark',
    'version': '1.0.0',
    'description': 'YouTube archiving made simple.',
    'long_description': '<!-- TODO: logo; #2 <https://github.com/Owez/yark/issues/2> -->\n<!-- TODO: add when logos done; #2 <https://github.com/Owez/yark/issues/2>: <h1 align="center">yark</h1> -->\n\n# yark\n\nYouTube archiving made simple.\n\n- [yark](#yark)\n  - [Installation](#installation)\n  - [Managing your Archive](#managing-your-archive)\n  - [Viewing your Archive](#viewing-your-archive)\n  - [Details](#details)\n\nYark lets you continuously archive all videos and metadata of a channel. You can also view your archive as a seemless offline website 🦾\n\n## Installation\n\nTo install yark, simply download Python 3.9+ and run the following:\n\n```shell\n$ pip3 install yark\n```\n\n## Managing your Archive\n\n\nOnce you\'ve installed yark, think of a name for your archive and copy the target\'s channel id:\n\n```shell\n$ yark new owez UCSMdm6bUYIBN0KfS2CVuEPA\n```\n\nNow that you\'ve created the archive, you can tell yark to download all videos and metadata:\n\n```shell\n$ yark refresh owez\n```\n\nHere\'s what my channel looked like after following the steps (if anything was updated/deleted it would be blue/red to indicate):\n\n<p><img src="https://raw.githubusercontent.com/Owez/yark/master/examples/images/report.png" alt="Report Demo" title="Report Demo" width="600" /></p>\n\n## Viewing your Archive\n\nViewing you archive is very simple, just type `view` and optionally the archive name:\n\n```shell\n$ yark view owez\n```\n\nThis will pop up an offline website in your browser letting you watch all videos 🚀\n\n<p><img src="https://raw.githubusercontent.com/Owez/yark/master/examples/images/channel.png" alt="Channel Demo" title="Channel Demo" /></p>\n\nUnder each video is a rich history report filled with graphs, as well as a noting feature which lets you add timestamped and permalinked comments 👐\n\n<p><img src="https://raw.githubusercontent.com/Owez/yark/master/examples/images/history.png" alt="History Demo" title="History Demo" /></p>\n\n## Details\n\nHere are some things to keep in mind when using yark; the good and the bad:\n\n- Don\'t create a new archive again if you just want to update it, yark accumulates all new metadata for you via timestamps\n- Feel free to suggest new features via the issues tab on this repository\n- Scheduling isn\'t a feature just yet, please use [`cron`](https://en.wikipedia.org/wiki/Cron) or something similar!\n',
    'author': 'Owen Griffiths',
    'author_email': 'root@ogriffiths.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/owez/yark',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
