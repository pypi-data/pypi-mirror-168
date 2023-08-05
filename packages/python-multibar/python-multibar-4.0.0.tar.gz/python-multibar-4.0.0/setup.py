# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multibar', 'multibar.api', 'multibar.impl']

package_data = \
{'': ['*']}

install_requires = \
['returns==0.19.0', 'termcolor==2.0.0']

setup_kwargs = {
    'name': 'python-multibar',
    'version': '4.0.0',
    'description': 'Flexible wrapper for static progressbar writing.',
    'long_description': '<div id="top"></div>\nProject: python-multibar\n<br>\nLicense: Apache 2.0\n<br>\nAbout: Tool for static progress bars writing.\n<br>\nOS: Independent\n<br>\nPython: 3.9+\n<br>\nTyping: Typed\n<br>\nTopic: Utilities\n<br />\n    <p align="center">\n    <br />\n    <a href="animatea.github.io/python-multibar/">Documentation</a>\n    ·\n    <a href="https://github.com/Animatea/python-multibar/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/Animatea/python-multibar/issues">Request Feature</a>\n    </p>\n<div id="top"></div>\n<p align="center">\n   <a href="i18n/ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>\n   <a href="i18n/ru_README.md"><img height="20" src="https://img.shields.io/badge/language-ru-green?style=social&logo=googletranslate"></a>\n</p>\n<details>\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#welcome-to-python-multibar!">Welcome to Python-Multibar</a>\n      <ul>\n        <li><a href="#installation">Installation</a></li>\n        <li><a href="#quickstart">Quickstart</a></li>\n        <li><a href="#documentation">Documentation</a></li>\n        <li><a href="#examples">Examples</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#contributing">Contributing</a>\n    </li>\n    <li>\n      <a href="#acknowledgments">Acknowledgments</a>\n    </li>\n  </ol>\n</details>\n\n# Welcome to Python-Multibar!\n<a href="https://dl.circleci.com/status-badge/redirect/gh/Animatea/python-multibar/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/python-multibar/tree/main.svg?style=svg"></a>\n<a href="https://pypi.org/project/tense/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/python-multibar"></a>\n<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>\n<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>\n\n### Installation\n```py\n# Unix/macOS users should use\n$ python -m pip install -U python-multibar\n\n# Windows users should use\n$ py -m pip install -U python-multibar\n```\n### Quickstart\n```py\n>>> import multibar\n\n>>> writer = multibar.ProgressbarWriter()\n>>> progressbar = writer.write(10, 100)\n# Using __str__() method, we get a progressbar\n# with a basic signature.\nOut: \'+-----\'\n\n# Writer returns progressbar object.\n>>> type(progressbar)\nOut: <class \'multibar.impl.progressbars.Progressbar\'>\n```\n### Documentation\nYou can access the documentation by clicking on the following link:\n- [animatea.github.io/python-multibar](animatea.github.io/python-multibar/)\n\n### Examples\nSome more of the features of python-multibar are in the project examples.\n<p align="center">\n<br />\n<a href="https://github.com/Animatea/python-multibar/tree/main/examples">Python-Multibar Examples</a>\n</p>\n<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>\n\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n> `NOTE:` before creating a pull request, you first need to install the project\'s dependencies:\n>  - `pip3 install -r dev-requirements.txt -r requirements.txt`\n>\n> Then go to the root directory of the project `...\\python-multibar>` and start all nox pipelines using the `nox` command.\n>\n> If all sessions are completed successfully, then feel free to create a pull request. Thanks for your PR\'s!\n\n<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>\n\n## Acknowledgments\n* [Choose an Open Source License](https://choosealicense.com)\n* [Img Shields](https://shields.io)\n* [GitHub Pages](https://pages.github.com)\n* [Python](https://www.python.org)\n* [Python Community](https://www.python.org/community/)\n* [MkDocs](https://www.mkdocs.org)\n* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)\n\n<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>\n\n',
    'author': 'DenyS',
    'author_email': 'animatea.programming@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Animatea/python-multibar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
