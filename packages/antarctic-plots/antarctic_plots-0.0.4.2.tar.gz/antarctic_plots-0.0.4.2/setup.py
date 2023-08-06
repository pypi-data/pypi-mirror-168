# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antarctic_plots', 'antarctic_plots.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pooch[progress]>=1.6.0,<2.0.0',
 'pyogrio>=0.4.1,<0.5.0',
 'pyproj>=3.3.1,<4.0.0',
 'rioxarray>=0.12.0,<0.13.0',
 'scipy>=1.7.1',
 'verde>=1.7.0,<2.0.0',
 'xarray[io]>=2022.6.0,<2023.0.0']

setup_kwargs = {
    'name': 'antarctic-plots',
    'version': '0.0.4.2',
    'description': 'Functions to automate Antarctic data visualization',
    'long_description': '<h1 align="center">Antarctic-plots</h1>\n<h2 align="center">Functions to automate Antarctic data visualization</h2>\n\n<p align="center">\n<a href="https://antarctic-plots.readthedocs.io/en/latest/"><strong>Documentation</strong> (dev)</a> •\n<a href="https://antarctic-plots.readthedocs.io/en/stable/"><strong>Documentation</strong> (stable)</a> •\n</p>\n\n<p align="center">\n<a href="https://mybinder.org/v2/gh/mdtanker/antarctic_plots/c88a23c9dfe92c36f0bfdbbc277d926c2de763de">\n <img src="https://img.shields.io/badge/launch-binder-579ACA.svg?logo=data:image/png;base64,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" alt="Binder link"></a>\n </p>\n \n<p align="center">\n<a href="https://pypi.org/project/antarctic-plots/"><img src="https://img.shields.io/pypi/v/antarctic-plots?style=flat-square" alt="Latest version on PyPI"></a>\n<a href="https://pypi.org/project/antarctic-plots/"><img src="https://img.shields.io/pypi/pyversions/antarctic-plots?style=flat-square" alt="Compatible Python versions."></a>\n<a href="https://zenodo.org/badge/latestdoi/475677039"><img src="https://zenodo.org/badge/475677039.svg?style=flat-square" alt="Zenodo DOI"></a>\n<a href="https://antarctic-plots.readthedocs.io/en/latest/index.html"><img src="https://img.shields.io/badge/jupyter-book-orange?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAZCAMAAAAVHr4VAAAAXVBMVEX////v7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/v7+/zdybv7+/zdybv7+/v7+/zdybv7+/zdybv7+/zdyaSmqV2AAAAHXRSTlMAEBAgIDAwQEBQUGBgcHCAgJCQoLCwwMDQ4ODw8MDkUIUAAADJSURBVHjaddAFkgNBCAXQP+7uAvc/5tLFVseYF8crUB0560r/5gwvjYYm8gq8QJoyIJNwlnUH0WEnART6YSezV6c5tjOTaoKdfGXtnclFlEBEXVd8JzG4pa/LDql9Jff/ZCC/h2zSqF5bzf4vqkgNwEzeClUd8uMadLE6OnhBFsES5niQh2BOYUqZsfGdmrmbN+TMvPROHUOkde8sEs6Bnr0tDDf2Roj6fmVfubuGyttejCeLc+xFm+NLuLnJeFAyl3gS932MF/wBoukfUcwI05kAAAAASUVORK5CYII=" alt="Jupyter Book"></a>\n </p>\n \n <p align="center">\n <a href=LICENSE><img src="https://img.shields.io/pypi/l/antarctic-plots?style=flat-square" alt="license"></a>\n <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/static/v1?label=code style&message=black&color=black&style=flat-square"></a>\n<a href=\'https://readthedocs.org/projects/antarctic-plots/\'><img src=\'https://readthedocs.org/projects/antarctic-plots/badge/?version=latest&style=flat-square\' alt=\'Documentation Status\' /></a>\n </p>\n\n![](docs/cover_fig.png)\n\n## Disclaimer\n\n<p align="center">\n🚨 **This package is in early stages of design and implementation.** 🚨\n </p>\n \nI welcome any feedback, ideas, or contributions! Please submit an [issue on Github](https://github.com/mdtanker/antarctic_plots/issues) for problems or feature ideas. \n\n## About\n\nThe **Antarctic-plots** python package provides some basic tools for creating maps and plots specific to Antarctica. It includes code to download common continent-wide datasets (i.e. Bedmap2, AntGG, ADMAP), and visualize them in a variety of ways, including cross sections and maps. Check out our [Documentation](https://antarctic-plots.readthedocs.io/en/latest/) for instructions on installing and using the package.\n\nFeel free to use, share, modify, and contribute to this project. I\'ve mostly made this for personal usage so expect significant changes and hopefully I\'ll implement some tests and more Gallery examples soon. \n\n## Project goals\n\nBelow is a list of some features I hope to eventually include. Feel free to make a feature request through [Github Issues](https://github.com/mdtanker/antarctic_plots/issues/new/choose).\n* Interactively choose profile locations by clicking on a map (See [Issue #1](https://github.com/mdtanker/antarctic_plots/issues/1))  \n* Create 3D interactive models to help visualize data.\n* Plot data in 3D\n* Include more Antarctic datasets to aid in download and storage.\n* Setup and online environment to run the package with needing Python on your computer (See [Issue #20](https://github.com/mdtanker/antarctic_plots/issues/20)) \n',
    'author': 'mdtanker',
    'author_email': 'matt.d.tankersley@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://antarctic-plots.readthedocs.io/en/latest/installation.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
