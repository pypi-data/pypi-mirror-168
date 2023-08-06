# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clophfit', 'clophfit.old']

package_data = \
{'': ['*'], 'clophfit.old': ['bash/*']}

install_requires = \
['click>=8.1.3',
 'corner>=2.2.1',
 'emcee>=3.1.1',
 'lmfit>=1.0.3',
 'numpy>=1.17',
 'openpyxl>=3.0.9',
 'pandas-stubs>=1.4.4.220912',
 'pandas>=1.3.3',
 'rpy2>=3.4.5',
 'scipy>=1.7.1',
 'seaborn>=0.11.2',
 'sympy>=1.9',
 'tqdm>=4.62.3',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['clop = clophfit.__main__:clop']}

setup_kwargs = {
    'name': 'clophfit',
    'version': '0.3.8',
    'description': 'Cli for fitting macromolecule pH titration or binding assays data e.g. fluorescence spectra.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/ClopHfit.svg)](https://pypi.org/project/ClopHfit/)\n[![Tests](https://github.com/darosio/ClopHfit/actions/workflows/tests.yml/badge.svg)](https://github.com/darosio/ClopHfit/actions/workflows/tests.yml)\n[![RtD](https://readthedocs.org/projects/clophfit/badge/)](https://clophfit.readthedocs.io/)\n[![zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.6354112.svg)](https://doi.org/10.5281/zenodo.6354112)\n\n# ClopHfit\n\nCli for fitting macromolecule pH titration or binding assay data, e.g.\nfluorescence spectra.\n\n-   Version: "0.3.8"\n\n## Features\n\n-   Plate Reader data Parser.\n-   Perform non-linear least square fitting.\n-   Extract and fit pH and chloride titrations of GFP libraries.\n    -   For 2 labelblocks (e.g. 400, 485 nm) fit data separately and\n        globally.\n    -   Estimate uncertainty using bootstrap.\n    -   Subtract buffer for each titration point.\n    -   Report controls e.g. S202N, E2 and V224Q.\n    -   Correct for dilution of titration additions.\n    -   Plot data when fitting fails and save txt file anyway.\n\n## Usage\n\n-   Extract and fit titrations from a list of tecan files collected at\n    various pH or chloride concentrations:\n\n        clop prtecan --help\n\n    For example:\n\n        clop prtecan list.pH -k ph --scheme ../scheme.txt --dil additions.pH --norm \\\n          --out prova2 --Klim 6.8,8.4 --sel 7.6,20\n\n    To reproduce older pr.tecan add [\\--no-weight]{.title-ref} option:\n\n        clop prtecan list.pH -k ph --scheme ../scheme.txt --no-bg --no-weight \\\n          --out 4old --Klim 6.8,8.4 --sel 7.6,20\n\n-   Predict chloride dissociation constant [K_d]{.title-ref} at given\n    pH:\n\n        clop eq1 --help\n\nTo use clophfit in a project:\n\n    from clophfit import prtecan, binding\n\n## Installation\n\nYou can get the library directly from\n[![PyPI](https://img.shields.io/pypi/v/ClopHfit.svg)](https://pypi.org/project/ClopHfit/):\n\n    pip install clophfit\n\n## Development\n\nPrepare a virtual development environment and test first installation:\n\n    pyenv install 3.10.2\n    poetry env use 3.10\n    poetry install\n    poetry run pytest -v\n\nMake sure:\n\n    pre-commit install\n    pre-commit install --hook-type commit-msg\n\nFor [Jupyter](https://jupyter.org/):\n\n    poetry run python -m ipykernel install --user --name="cloph-310"\n\nTo generate docs:\n\n    poetry run nox -rs docs\n\nWhen needed (e.g. API updates):\n\n    sphinx-apidoc -f -o docs/api/ src/clophfit/\n\nUse commitizen and github-cli to release:\n\n    poetry run cz bump --changelog-to-stdout --files-only (--prerelease alpha) --increment MINOR\n    gh release create (--target devel) v0.3.0a0\n\nRemember!!! Update::\n- ClopHfit/docs/requirements.txt\n- ClopHfit/.github/workflows/constraints.txt\n\n### Development environment\n\n-   Test automation requires nox and nox-poetry.\n\n-   Formatting with black\\[jupyter\\] configured in pyproject.\n\n-   Linters are configured in .flake8 .darglint and .isort.cfg and\n    include:\n\n        - flake8-isort\n        - flake8-bugbear\n        - flake8-docstrings\n        - darglint\n        - flake8-eradicate\n        - flake8-comprehensions\n        - flake8-pytest-style\n        - flake8-annotations (see mypy)\n        - flake8-rst-docstrings\n\n    > -   rst-lint\n\n-   pre-commit configured in .pre-commit-config.yaml activated with:\n\n        - pre-commit install\n        - commitizen install --hook-type commit-msg\n\n-   Tests coverage (pytest-cov) configured in .coveragerc.\n\n-   Type annotation configured in mypy.ini.\n\n-   [Commitizen](https://commitizen-tools.github.io/commitizen/) also\n    used to bump version:\n\n        cz bump --changelog-to-stdout --files-only --prerelease alpha --increment MINOR\n\n    -   need one-time initialization:\n\n            (cz init)\n\n-   xdoctest\n\n-   sphinx with pydata-sphinx-theme and sphinx-autodoc-typehints.\n    (nbsphinx, sphinxcontrib-plantuml):\n\n        mkdir docs; cd docs\n        sphinx-quickstart\n\n    Edit conf.py \\[\\"sphinx.ext.autodoc\\"\\] and index.rst \\[e.g.\n    api/modules\\]:\n\n        sphinx-apidoc -f -o docs/api/ src/clophfit/\n\n-   CI/CD configured in .github/workflows:\n\n        tests.yml\n        release.yml\n\n    Remember to update tools version e.g. nox_poetry==0.9.\n\n### What is missing to [modernize](https://cjolowicz.github.io/posts/hypermodern-python-06-ci-cd/):\n\n-   coveralls/Codecov\n-   release drafter; maybe useful when merging pr into main.\n-   readthedocs or ghpages?\n    <https://www.docslikecode.com/articles/github-pages-python-sphinx/>\n\n## Code of Conduct\n\nEveryone interacting in the readme_renderer project\\\'s codebases, issue\ntrackers, chat rooms, and mailing lists is expected to follow the [PSF\nCode of\nConduct](https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md).\n',
    'author': 'daniele arosio',
    'author_email': 'daniele.arosio@cnr.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/darosio/ClopHfit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
