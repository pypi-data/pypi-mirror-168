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
    'version': '1.1.2.1',
    'description': 'Colibrie is a blazing fast tool to extract tables from PDFs',
    'long_description': '# Colibrie\n [![image](https://img.shields.io/pypi/v/colibrie.svg)](https://pypi.org/project/colibrie/) [![image](https://img.shields.io/pypi/l/colibrie.svg)](https://pypi.org/project/colibrie/)\n\nColibrie is a blazing fast tool to extract tables from PDFs \n\n## Why Colibrie?\n\n- :rocket: **Efficient**: Colibrie is faster by multiple order of magnitude than any actual existing solution\n- :sparkles: **Fidel visual**: Colibrie can provide 1:1 HTML representation of any tables it\'ll find\n- :books: **Reliable**: Colibri will find every valid tables without exception if the PDF is compatible with the core principle of Colibrie\n- :memo: **Output**: Each table can be export into to multiple formats, which include : \n  - Pandas Dataframe.\n  - HTML.\n\n### Benchmark :\nSome number to compare [Camelot](https://github.com/camelot-dev/camelot) (a popular library to extract tables from PDF) and Colibrie\n<table>\n  <thead>\n    <tr>\n        <th colspan="2"></th>\n        <th colspan="4">Tables extracted</th>\n        <th colspan="2"></th>\n    </tr>\n    <tr>\n        <th colspan="2">Times in second</th>\n        <th colspan="2">camelot</th>\n        <th colspan="2">colibrie</th>\n        <th colspan="2"></th>\n    </tr>\n    <tr style="text-align: right;">\n      <th>camelot</th>\n      <th>colibrie</th>\n      <th>valid</th>\n      <th>false positive</th>\n      <th>valid</th>\n      <th>false positive</th>\n      <th>pages count</th>\n      <th>pdf file</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>0.53</td>\n      <td>0.00545</td>\n      <td>1</td>\n      <td>0</td>\n      <td>1</td>\n      <td>0</td>\n      <td>1</td>\n      <td><a href="https://github.com/abitoun-42/colibrie/files/9620468/boc_20220014_0001_p000_extract_2.pdf">small pdf</a></td>\n    </tr>\n    <tr>\n      <td>5.95</td>\n      <td>0.02100</td>\n      <td>4</td>\n      <td>0</td>\n      <td>4</td>\n      <td>0</td>\n      <td>11</td>\n      <td><a href="https://github.com/abitoun-42/colibrie/files/9620506/boc_20210034_0000_0003.pdf">medium pdf</a></td>\n    </tr>\n    <tr>\n      <td>105.00</td>\n      <td>0.21900</td>\n      <td>62</td>\n      <td>1</td>\n      <td>62</td>\n      <td>0</td>\n      <td>167</td>\n      <td><a href="https://github.com/abitoun-42/colibrie/files/9620511/boc_20220014_0001_p000.pdf">big pdf</a></td>\n    </tr>\n    <tr>\n      <td>182.00</td>\n      <td>0.69000</td>\n      <td>175</td>\n      <td>1</td>\n      <td>177</td>\n      <td>0</td>\n      <td>269</td>\n      <td><a href="https://github.com/abitoun-42/colibrie/files/9620515/boc_20220025_0001_p000.pdf">giant pdf</a></td>\n    </tr>\n  </tbody>\n</table>\n\n## Installation\n\n### using source\n```\npip install poetry\n\ngit clone https://github.com/abitoun-42/colibrie.git\n\ncd colibrie\n\npoetry install\n```\n### using pip\n```\npip install colibrie\n```\n\n## Usage\n```\nfrom colibrie.extract_tables import extract_table\n\ntables = extract_table(\'pdf_path\')\n```\n',
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
