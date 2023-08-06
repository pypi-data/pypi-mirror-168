# legend-testdata-py

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/legend-exp/legend-testdata-py?logo=git)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/legend-exp/legend-testdata-py/legend-testdata/main?label=main%20branch&logo=github)](https://github.com/legend-exp/legend-testdata-py/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Codecov](https://img.shields.io/codecov/c/github/legend-exp/legend-testdata-py?logo=codecov)](https://app.codecov.io/gh/legend-exp/legend-testdata-py)
![GitHub issues](https://img.shields.io/github/issues/legend-exp/legend-testdata-py?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr/legend-exp/legend-testdata-py?logo=github)
![License](https://img.shields.io/github/license/legend-exp/legend-testdata-py)

Tiny Python package to access [LEGEND test data](https://github.com/legend-exp/legend-testdata). Usage:

```py
from legend_testdata import LegendTestData

ldata = LegendTestData()  # clone legend-exp/legend-testdata below /tmp
ldata.checkout("968c9ba")  # optionally checkout a specific version
ldata.get_path("orca/fc/L200-comm-20220519-phy-geds.orca")  # get absolute path to test file
ldata.reset()  # checkout default branch (main)
```

<sub>*This Python package layout is based on [pyproject-template](https://github.com/gipert/pyproject-template).*</sub>
