# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autorequests', 'autorequests.parsing']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.5.1,<13.0.0']

entry_points = \
{'console_scripts': ['autorequests = autorequests.__main__:cli']}

setup_kwargs = {
    'name': 'autorequests',
    'version': '2.0.0',
    'description': 'Generate Python code to recreate a request from your browser.',
    'long_description': '<h1 align=center>AutoRequests</h1>\n<p align=center>\n  <span>Generate Python code to recreate a request from your browser.</span>\n  <br>\n\n  <a title="PyPI - Version" href="https://pypi.org/project/autorequests/" target="_blank">\n    <img src="https://img.shields.io/pypi/v/autorequests?color=390099&style=for-the-badge"/>\n  </a>\n\n  <a title="PyPI - Python Version" href="https://www.python.org/downloads/" target="_blank">\n     <img src="https://img.shields.io/pypi/pyversions/autorequests?color=B80068&style=for-the-badge&logo=python&logoColor=fff"/>\n  </a>\n\n  <a title="License - MIT" href="LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/Hexiro/autorequests?style=for-the-badge&color=390099&labelColor=474747">\n  </a>\n\n  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/Hexiro/autorequests/tests?logo=github&style=for-the-badge&label=tests">\n  <br>\n</p>\n\n### 📺 Demo\n\n<img alt="Demo" src="https://user-images.githubusercontent.com/42787085/191134993-85750fc2-b13e-4e70-939b-2dcc2f1785b2.gif"/>\n\n### 💼 Example Use Cases\n\n- Creating a foundation for an API wrapper\n- Recreating a request outside the browser\n- Testing what cookies or headers are required for a server to understand your request\n\n### ✂️ How to Copy\n\n1. Inspect Element\n2. Go to `Network` tab\n3. Find web request\n4. Right-Click\n5. Copy\n6. Choose one of the following:\n   1. Powershell\n   2. Node.js fetch\n\n## 📦 Installation\n\ninstall the package with pip\n\n```\n$ pip install autorequests\n```\n\nor download the latest development build from GitHub\n\n```\n$ pip install -U git+https://github.com/Hexiro/autorequests\n```\n\n## 🖥️ Command Line\n\n```console\n$ autorequests --help\n```\n\nMeta Options\n\n```console\n  --file  -f            Optional file to read input from.\n  --copy  -c            Copy the output to the clipboard\n```\n\ngeneration options\n\n```console\n  -sync/--async  -s/-a  Generate synchronous or asynchronous code.\n  --httpx        -h     Use httpx library to make requests.\n  --no-headers   -nh    Don\'t include headers in the generated output.\n  --no-cookies   -nc    Don\'t include cookies in the generated output.\n```\n\n## 🐞 Contributing\n\nsee [CONTRIBUTING.md](./CONTRIBUTING.md)\n',
    'author': 'Hexiro',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Hexiro/autorequests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
