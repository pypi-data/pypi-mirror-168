# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maser',
 'maser.data',
 'maser.data.base',
 'maser.data.cdpp',
 'maser.data.cdpp.interball',
 'maser.data.cdpp.viking',
 'maser.data.cdpp.wind',
 'maser.data.ecallisto',
 'maser.data.nancay',
 'maser.data.nancay.nda',
 'maser.data.nancay.nenufar',
 'maser.data.padc',
 'maser.data.padc.cassini',
 'maser.data.padc.juno',
 'maser.data.pds',
 'maser.data.pds.co',
 'maser.data.pds.vg',
 'maser.data.psa',
 'maser.data.psa.labels',
 'maser.data.psa.mex',
 'maser.data.rpw']

package_data = \
{'': ['*'], 'maser.data.psa.labels': ['MEX-M-MARSIS-3-RDR-AIS-V1.0/*']}

install_requires = \
['astropy>=5.0.4,<6.0.0', 'numpy>=1.23.0,<2.0.0', 'xarray>=2022.3.0,<2023.0.0']

extras_require = \
{'all': ['spacepy>=0.4.0,<0.5.0',
         'nenupy>=2.1.0,<3.0.0',
         'jupyter>=1.0.0,<2.0.0',
         'jupytext>=1.13.8,<2.0.0'],
 'jupyter': ['jupyter>=1.0.0,<2.0.0', 'jupytext>=1.13.8,<2.0.0'],
 'nenupy': ['nenupy>=2.1.0,<3.0.0'],
 'spacepy': ['spacepy>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'maser.data',
    'version': '0.3.0',
    'description': 'Maser4py submodule to handle radio data',
    'long_description': '# About maser.data\n\nmaser.data is a submodule of [maser4py](https://pypi.org/project/maser4py/).\n\nIt offers programs to handle radio data from the following missions:\n\n- Cassini\n- Ecallisto\n- Interball\n- Juno\n- Mars Express\n- nancay decametric array (Jupiter only)\n- Nancay NenuFAR/BST\n- Solar orbiter\n- Viking\n- Wind\n\n# Installation\n\nTo install the package, run the following command:\n\n```\npip install maser.data\n```\n\nor use one of the extra options:\n\n- `jupyter` for Jupyter notebook support\n- `spacepy` for CDF data format support (note that this requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html))\n- `nenupy` for NenuFAR data products support\n- `all` to install all the above\n\nFor example use `maser.data[jupyter,spacepy]` if you want to use `maser.data` with spacepy and jupyter notebooks:\n\n```bash\npip install maser.data[jupyter,spacepy]\n```\n\n# Usage\n\nThe `Data` class is a wrapper around several classes that allow you to read data from many different formats, including CDF, Fits, and some custom binary formats. By default, the class will try to automagically detect the format of the file and use the appropriate class to read the data.\n\n```python\nfrom maser.data import Data\n\nfilepath = "path/to/my/data/file.ext"\ndata = Data(filepath=filepath)\n```\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/namespace) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).\n\n# Development\n\nTo contribute to the development of the package, you will need to install a local copy of maser.data\n\n```\ngit clone https://gitlab.obspm.fr/maser/maser4py.git\n```\n\nThen, you can install the package locally\n\n## Requirements\n\n`maser.data` requirements are detailed in the `pyproject.toml` file\n\n### poetry\n\nTo install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):\n\n```\npip install poetry\n```\n\n### CDF file format\n\nTo use `maser.data` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.\n\n## Installing a local copy of maser.data\n\nUse the following command to install the package:\n\n```bash\npoetry install\n```\n\nor this one if you want to use `maser.data` with spacepy to handle CDF files:\n\n```bash\npoetry install --extras "spacepy"\n```\n\n## Tests\n\nUse `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).\n\n## Generate setup.py for editable local installation\n\nThe `setup.py` file have to be updated after any changes to the `pyproject.toml` file.\n\nTo generate a new `setup.py` file, go to the top level of the `maser.data` project folder and run:\n\n```\npython generate_setup.py\n```\n\nNow you can use the `setup.py` file to install the package locally in editable mode:\n\n```\npip install -e path/to/project/folder\n```\n\n## Build the documentation\n\nUse `sphinx-build docs/source docs/public` to build the documentation.\n\n## Manually publish `maser` and generate a new DOI\n\nTo publish `maser` with `poetry` you will have to build a `dist` package:\n\n```\npoetry build\n```\n\nAnd then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):\n\n```\npoetry publish\n```\n\n`maser` comes with a Python client (see `.ci/zenodo.py`) to interact with the Zenodo API and generate automatically a DOI for each new version of `maser`.\n\nTo archive `maser` on Zenodo:\n\n1. [Create an access token](https://zenodo.org/account/settings/applications/tokens/new/)\n2. Is this the first maser deposit on Zenodo ?\n\n- Yes it\'s the first deposit, so you don\'t need any ID\n- No, it\'s a new version of `maser`. Then browse to the first record of maser on Zenodo and check the URL : `https://zenodo.org/record/<DEPOSITION_ID>` to get the `maser` deposition ID.\n\n3. Use the following command to deposit the package on Zenodo:\n\n```bash\n python .ci/zenodo.py -p ./ -t <ACCESS_TOKEN> -a ./dist/maser4py-X.Y.Z.tar.gz  -id <DEPOSITION_ID>\n```\n\n4. Browse to the `maser` record on Zenodo, check the metadata/files and publish the package to finally generate the DOI.\n\nNotes :\n\n- the `--sandbox` keyword can be used to deposit files on the Zenodo test server\n- the `--publish` keyword can be used to automatically publish the new record and generate the DOI. But **be careful**, once published, there is no way to modify a record on Zenodo without publishing a new version.\n',
    'author': 'Baptiste Cecconi',
    'author_email': 'baptiste.cecconi@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
