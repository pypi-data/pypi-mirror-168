# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maser']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['jupyter>=1.0.0,<2.0.0',
         'jupytext>=1.13.8,<2.0.0',
         'maser.data>=0.3.0,<0.4.0',
         'maser.plot>=0.2.0,<0.3.0'],
 'data': ['maser.data>=0.3.0,<0.4.0'],
 'jupyter': ['jupyter>=1.0.0,<2.0.0', 'jupytext>=1.13.8,<2.0.0'],
 'plot': ['maser.plot>=0.2.0,<0.3.0']}

entry_points = \
{'console_scripts': ['maser = maser.script:main']}

setup_kwargs = {
    'name': 'maser4py',
    'version': '0.13.0',
    'description': 'maser4py offers tools to handle low frequency radioastronomy data',
    'long_description': '# About maser4py\n\nmaser4py offers modules to hande data from several space and ground radio observatory.\n\nIt comes with the following submodules:\n\n- [maser.data](https://pypi.org/project/maser.data/) for radio data parsing features\n- [maser.plot](https://pypi.org/project/maser.plot/) for radio data plotting features\n\nmaser4py is developed in the framework of the [MASER project](https://maser.lesia.obspm.fr).\n\n# Installation\n\nTo install the package, run the following command:\n\n```\npip install maser4py\n```\n\nor use one of the extra options:\n\n- `jupyter` for Jupyter notebook support\n- `jupytext` for Jupyter notebook text support\n- `data` for [maser.data](https://pypi.org/project/maser.data/) submodule features\n- `plot` for [maser.plot](https://pypi.org/project/maser.plot/) submodule features\n- `all` to install all the above\n\nFor example if you want to use `maser4py` with maser.data and maser.plot submodules:\n\n```bash\npip install maser4py[data,plot]\n```\n\n# Usage\n\nExamples of usage can be found in the `examples` folder.\n\nExamples can also be run as Jupyter notebooks on Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/namespace) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).\n\n# Development\n\nTo contribute to the development of the package, you will need to install a local copy of maser4py:\n\n```\ngit clone https://gitlab.obspm.fr/maser/maser4py.git\n```\n\nThen, you can install the package locally\n\n## Requirements\n\n`maser4py` requirements are detailed in the `pyproject.toml` file\n\n### poetry\n\nTo install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):\n\n```\npip install poetry\n```\n\n### CDF file format\n\nTo use `maser4py` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.\n\n## Installing a local copy of maser4py\n\nUse the following command to install the package:\n\n```bash\npoetry install\n```\n\n## Tests\n\nUse `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).\n\n## Generate setup.py for editable local installation\n\nThe `setup.py` file have to be updated after any changes to the `pyproject.toml` file.\n\nTo generate a new `setup.py` file, go to the top level of the `maser4py` project folder and run:\n\n```\npython generate_setup.py\n```\n\nNow you can use the `setup.py` file to install the package locally in editable mode:\n\n```\npip install -e path/to/project/folder\n```\n\n## Build the documentation\n\nUse `sphinx-build docs/source docs/public` to build the documentation.\n\n## Manually publish `maser` and generate a new DOI\n\nTo publish `maser` with `poetry` you will have to build a `dist` package:\n\n```\npoetry build\n```\n\nAnd then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):\n\n```\npoetry publish\n```\n\n`maser` comes with a Python client (see `.ci/zenodo.py`) to interact with the Zenodo API and generate automatically a DOI for each new version of `maser`.\n\nTo archive `maser` on Zenodo:\n\n1. [Create an access token](https://zenodo.org/account/settings/applications/tokens/new/)\n2. Is this the first maser deposit on Zenodo ?\n\n- Yes it\'s the first deposit, so you don\'t need any ID\n- No, it\'s a new version of `maser`. Then browse to the first record of maser on Zenodo and check the URL : `https://zenodo.org/record/<DEPOSITION_ID>` to get the `maser` deposition ID.\n\n3. Use the following command to deposit the package on Zenodo:\n\n```bash\n python .ci/zenodo.py -p ./ -t <ACCESS_TOKEN> -a ./dist/maser4py-X.Y.Z.tar.gz  -id <DEPOSITION_ID>\n```\n\n4. Browse to the `maser` record on Zenodo, check the metadata/files and publish the package to finally generate the DOI.\n\nNotes :\n\n- the `--sandbox` keyword can be used to deposit files on the Zenodo test server\n- the `--publish` keyword can be used to automatically publish the new record and generate the DOI. But **be careful**, once published, there is no way to modify a record on Zenodo without publishing a new version.\n',
    'author': 'Xavier BONNIN',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/maser4py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
