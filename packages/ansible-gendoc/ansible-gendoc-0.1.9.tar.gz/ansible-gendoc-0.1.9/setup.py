# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_gendoc']

package_data = \
{'': ['*'], 'ansible_gendoc': ['templates/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'giturlparse>=0.10.0,<0.11.0',
 'importlib-metadata>=4.12.0,<5.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ansible-gendoc = ansible_gendoc.main:app']}

setup_kwargs = {
    'name': 'ansible-gendoc',
    'version': '0.1.9',
    'description': 'Ansible-gendoc build documentation of Ansible Roles.',
    'long_description': "# Ansible-Gendoc\n\n*Inspired by Felix Archambault's* [ansidoc](https://github.com/archf/ansidoc)\nproject.\n\nAn [example](example.md) generated with `ansible-gendoc`.\n\n## Features\n\n* Generate the documentation for a role located in a directory\n* Can use a personal template `README.j2` present in folder `templates`\n\n## Quickstart\n\nIf you have an existing README.md file in your role, backup it before !\n\n### Run From docker\n\nClone this project and build the image :\n\n```bash\ngit clone\nexport DOCKER_BUILDKIT=1\ndocker build . -t ansible-gendoc:0.1.0 -t ansible-gendoc:latest\ndocker run --user $(id -u):$(id -g) -it ansible-gendoc:latest help\n```\n\n### Install python package\n\nInstall the latest version `ansible-gendoc` with `pip` or `pipx`\n\n```bash\npip install ansible-gendoc\n```\n\n### Usage\n\n```bash\nansible-gendoc --help\n\n Usage: ansible-gendoc [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ────────────────────────────────────────────────────────────────────────╮\n│ --version             -v        Show the application's version and exit.         │\n│ --install-completion            Install completion for the current shell.        │\n│ --show-completion               Show completion for the current shell, to copy   │\n│                                 it or customize the installation.                │\n│ --help                          Show this message and exit.                      │\n╰──────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────────╮\n│ init     Copy templates README.j2 from packages in templates/role folder.        │\n│ render   Build the Documentation                                                 │\n╰──────────────────────────────────────────────────────────────────────────────────╯\n```\n\n#### Build your first documentation of a role\n\nTo build the documentation roles, you can run these commands :\n\n* with package installed with pip\n  `ansible-gendoc render`.\n* with docker images\n  `docker run --user $(id -u):$(id -g) -v <path_role>:/role -it ansible-gendoc:latest render role`.\n\n#### Use your personal template\n\nTo use a personal template, you need to `init` the template in the templates\nfolder of your role. If `ansible-gendoc` find an existing file\n`templates/README.j2`, it will use it to render the README.md file.\n\n```bash\nansible-gendoc init\nls templates\nREADME.j2\n```\n\nThe template use [`jinja`](https://jinja.palletsprojects.com/) as templating\nlanguage.\n\nModify it, for example replace `html` or `Restructuredtext` or another language.\nYou can remove some variables too.\n\n#### Documentation of vars template\n\nThe documentation of vars coming soon.\n",
    'author': 'Stephane ROBERT',
    'author_email': 'stephane.robert@fr.clara.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.claranet.fr/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
