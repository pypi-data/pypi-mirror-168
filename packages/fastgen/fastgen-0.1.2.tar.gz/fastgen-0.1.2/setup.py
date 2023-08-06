# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastgen', 'fastgen.managers']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3',
 'pre-commit>=2.20.0,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['fastgen = fastgen.main:app']}

setup_kwargs = {
    'name': 'fastgen',
    'version': '0.1.2',
    'description': 'FastGen, Start FastAPI Projects In Lightning Speed',
    'long_description': '# ⚡ _**FastGen**_\n\nStart FastAPI Projects in Lightning Speed\n\nBuilt With **Typer** To Help With <span style="color:green">**FastAPI**</span>.\n\n## 👀 **Take A Look**\n\nthis is a glanc of the project structure you will have once you use **FastGen**\n\n![dirs_images](./docs/dir.png)\n\n## ✨ **Installation**\n\n```console\n$ python -m pip install fastgen\n```\n\n**Usage**:\n\n```console\n$ fastgen [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `info`\n- `new`\n\n## `fastgen info`\n\n**Usage**:\n\n```console\n$ fastgen info [OPTIONS]\n```\n\n**Options**:\n\n- `--help`: Show this message and exit.\n\n## `fastgen new`\n\n**Usage**:\n\n```console\n$ fastgen new [OPTIONS] ⭐ Project Name\n```\n\n**Arguments**:\n\n- `⭐ Project Name`: [required]\n\n**Options**:\n\n- `--dir 📁 Directory Path`\n- `--package-manager 📦 Package Manager`: [default: pip]\n  ( Options are pip , poetry "Comming Soon" )\n- `--migrations / --no-migrations`: [default: False]\n- `--docker / --no-docker`: [default: False]\n- `--testing / --no-testing`: [default: False]\n- `--database 📅 Database`: [default: postgresql] ( Options are postgresql,mysql,sqlite )\n- `--help`: Show this message and exit.\n\n## 🪲 **Encountered A Problem !**\n\nfeel free to open an issue discussing the problem you faced\n\n## 🤝🏻 **Contributing**\n\nplease refer to [Contribution Guide](./CONTRIBUTING.md)\n',
    'author': 'kareem',
    'author_email': 'kareemmahlees@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kareemmahlees/fastgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
