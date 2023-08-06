# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docx_form',
 'docx_form.constants',
 'docx_form.content_controls',
 'docx_form.enums',
 'docx_form.globals',
 'docx_form.type_aliases']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.1.1,<6.0.0', 'lxml>=4.9.1,<5.0.0', 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'docx-form',
    'version': '0.1.3',
    'description': 'DO NOT USE, THIS IS A WORK IN PROGRESS -- A library that allows the editing of form XML components in .docx files.',
    'long_description': 'None',
    'author': 'Reece Bourgeois',
    'author_email': 'reecebourgeois@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
