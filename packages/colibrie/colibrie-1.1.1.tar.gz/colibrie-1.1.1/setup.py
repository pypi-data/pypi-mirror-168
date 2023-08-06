# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colibrie']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.32,<0.30.0',
 'Pillow>=9.2.0,<10.0.0',
 'PyMuPDF>=1.20.2,<2.0.0',
 'ailist>=1.0.4,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'colibrie',
    'version': '1.1.1',
    'description': 'Colibrie is a blazing fast repository to extract tables from PDF files',
    'long_description': "# Colibrie\nColibrie is a blazing fast repository to extract tables from PDF files \n\n# Installation\n```\npip install colibrie\n```\n\n# Usage\n```\nfrom colibrie.extract_tables import extract_table\n\ntables = extract_table('pdf_path')\n```",
    'author': 'Alexandre Bitoun',
    'author_email': 'alexandre.bitoun@outlook.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/abitoun-42/colibrie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
