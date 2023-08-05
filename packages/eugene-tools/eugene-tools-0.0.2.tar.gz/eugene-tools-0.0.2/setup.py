# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eugene',
 'eugene.cli',
 'eugene.dataload',
 'eugene.dataload.dataloaders',
 'eugene.dataload.motif',
 'eugene.datasets',
 'eugene.evaluate',
 'eugene.external',
 'eugene.external.gkm_svm',
 'eugene.external.janggu',
 'eugene.external.janggu.data',
 'eugene.external.kipoi',
 'eugene.external.kipoi.kipoi_veff',
 'eugene.external.sklearn',
 'eugene.interpret',
 'eugene.models',
 'eugene.models.base',
 'eugene.plot',
 'eugene.preprocess',
 'eugene.train',
 'eugene.utils']

package_data = \
{'': ['*'],
 'eugene.datasets': ['random1000/*'],
 'eugene.external.janggu': ['resources/*']}

install_requires = \
['captum>=0.5.0,<0.6.0',
 'h5py>=3.7.0,<4.0.0',
 'ipywidgets>=7.6.5,<8.0.0',
 'jsonargparse[signatures]==4.12.0',
 'logomaker>=0.8,<0.9',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pyranges>=0.0.117,<0.0.118',
 'pytorch-lightning==1.5.10',
 'questionary>=1.10.0,<2.0.0',
 'rich>=12.4.4,<13.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'seqlogo>=5.29.8,<6.0.0',
 'sphinx-autodoc-typehints[docs]>=1.19.2,<2.0.0',
 'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0',
 'torch-tb-profiler>=0.4.0,<0.5.0',
 'torch>=1.11.0,<2.0.0',
 'torchvision>=0.12,<0.13',
 'umap-learn>=0.5.3,<0.6.0',
 'vizsequence>=0.1.1,<0.2.0',
 'wget>=3.2,<4.0',
 'xlrd>=2.0.1,<3.0.0',
 'yuzu-ism>=0.0.1,<0.0.2']

extras_require = \
{':extra == "dev"': ['black[dev]>=22.3,<23.0',
                     'pre-commit[dev]>=2.20,<3.0',
                     'pytest[dev]>=7.1.2,<8.0.0',
                     'codecov[dev]>=2.0.8,<3.0.0'],
 ':extra == "docs"': ['Sphinx[docs]==5.1.1',
                      'myst-parser[docs]==0.18.0',
                      'sphinxcontrib-apidoc[docs]==0.3.0',
                      'sphinx-autobuild[docs]==2021.3.14',
                      'autopep8[docs]==1.6.0'],
 ':extra == "janggu"': ['pyBigWig[janggu]>=0.3.18,<0.4.0',
                        'pybedtools[janggu]>=0.9.0,<0.10.0',
                        'biopython[janggu]==1.77',
                        'progress[janggu]>=1.6,<2.0',
                        'keras[janggu]>=2.4.3,<3.0.0',
                        'tensorflow[janggu]>=2.4.1,<3.0.0'],
 ':extra == "kipoi"': ['Shapely[kipoi]>=1.8.1,<2.0.0',
                       'kipoi[kipoi]>=0.8.6,<0.9.0',
                       'kipoiseq[kipoi]>=0.7.1,<0.8.0'],
 ':extra == "memesuite"': ['pyjaspar[memesuite]>=2.1.0,<3.0.0',
                           'pymemesuite[memesuite]>=0.1.0a1,<0.2.0']}

setup_kwargs = {
    'name': 'eugene-tools',
    'version': '0.0.2',
    'description': 'A Python toolkit for predictive analyses of regulatory sequences ',
    'long_description': "# EUGENE (**E**lucidating and **U**nderstanding **G**rammar of **E**lements with **Ne**uralnets)\n\nEUGENe represents a computational framework for machine learning based modeling of regulatory sequences. It is designed after the [Scanpy](https://scanpy.readthedocs.io/en/stable/) package for single cell analysis in Python and is meant to make the development of deep learning worlflows in the genomics field more findable, accessible, interoperitable and reproducible (FAIR). EUGENe consists of several modules for handling data and for building, training, evaluating and interpreting deep learners that predict annotations of biological sequences. EUGENe is primarily designed to be used through its Python API and we feel that users will get the most out of it by using a notebook interface (i.e. Jupyter).\n\nEUGENe is a package that is still active development, so there's a good chance you'll hit an error to if you use EUGENe before its first stable release. However, catching these errors is incredbily valuable for us! If you run into such errors or have any questions, please open an issue! You can read the [current documentation]() here for getting started.\n",
    'author': 'Adam Klie',
    'author_email': 'aklie@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.12,<3.11',
}


setup(**setup_kwargs)
