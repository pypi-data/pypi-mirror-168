# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covsirphy',
 'covsirphy._deprecated',
 'covsirphy.downloading',
 'covsirphy.dynamics',
 'covsirphy.engineering',
 'covsirphy.gis',
 'covsirphy.science',
 'covsirphy.util',
 'covsirphy.visualization']

package_data = \
{'': ['*']}

install_requires = \
['AutoTS>=0.5.0,<0.6.0',
 'Unidecode>=1.3.4,<2.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'country-converter>=0.7.7,<0.8.0',
 'geopandas>=0.11.1,<0.12.0',
 'japanmap>=0.0.21,<0.0.25',
 'lightgbm>=3.3.2,<4.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'optuna>=3.0.1,<4.0.0',
 'p-tqdm>=1.4.0,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pca>=1.8.3,<2.0.0',
 'pyarrow>=9.0.0,<10.0.0',
 'requests>=2.28.1,<3.0.0',
 'ruptures>=1.1.7,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.8.1',
 'seaborn>=0.12.0,<0.13.0',
 'tabulate>=0.8.10,<0.9.0',
 'wbdata>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'covsirphy',
    'version': '2.27.0',
    'description': 'COVID-19 data analysis with phase-dependent SIR-derived ODE models',
    'long_description': '\n<img src="https://raw.githubusercontent.com/lisphilar/covid19-sir/master/docs/logo/covsirphy_headline.png" width="390" alt="CovsirPhy: COVID-19 analysis with phase-dependent SIRs">\n\n[![PyPI version](https://badge.fury.io/py/covsirphy.svg)](https://badge.fury.io/py/covsirphy)\n[![Downloads](https://pepy.tech/badge/covsirphy)](https://pepy.tech/project/covsirphy)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/covsirphy)](https://badge.fury.io/py/covsirphy)\n[![GitHub license](https://img.shields.io/github/license/lisphilar/covid19-sir)](https://github.com/lisphilar/covid19-sir/blob/master/LICENSE)\n[![Quality Check](https://github.com/lisphilar/covid19-sir/actions/workflows/test.yml/badge.svg)](https://github.com/lisphilar/covid19-sir/actions/workflows/test.yml)\n[![Test Coverage](https://codecov.io/gh/lisphilar/covid19-sir/branch/master/graph/badge.svg?token=9Z8Z1UHY3I)](https://codecov.io/gh/lisphilar/covid19-sir)\n\n# CovsirPhy introduction\n\n[<strong>Documentation</strong>](https://lisphilar.github.io/covid19-sir/index.html)\n| [<strong>Installation</strong>](https://lisphilar.github.io/covid19-sir/INSTALLATION.html)\n| [<strong>Tutorial</strong>](<https://lisphilar.github.io/covid19-sir/01_data_preparation.html>)\n| [<strong>API reference</strong>](https://lisphilar.github.io/covid19-sir/covsirphy.html)\n| [<strong>GitHub</strong>](https://github.com/lisphilar/covid19-sir)\n| [<strong>Qiita (Japanese)</strong>](https://qiita.com/tags/covsirphy)\n\n<strong>CovsirPhy is a Python library for infectious disease (COVID-19: Coronavirus disease 2019, Monkeypox 2022) data analysis with phase-dependent SIR-derived ODE models. We can download datasets and analyze them easily. Scenario analysis with CovsirPhy enables us to make data-informed decisions. </strong>\n\n## Inspiration\n\n* Monitor the spread of COVID-19/Monkeypox with SIR-derived ODE models\n* Predict the number of cases in each country/province\n* Find the relationship of reproductive number and measures taken by each country\n\n<strong>If you have ideas or need new functionalities, please join this project.\nAny suggestions with [Github Issues](https://github.com/lisphilar/covid19-sir/issues/new/choose) and [Twitter: @lisphilar](https://twitter.com/lisphilar) are always welcomed. Questions are also great. Please refer to [Guideline of contribution](https://lisphilar.github.io/covid19-sir/CONTRIBUTING.html).</strong>\n\n## Installation\n\nThe latest stable version of CovsirPhy is available at [PyPI (The Python Package Index): covsirphy](https://pypi.org/project/covsirphy/) and supports Python 3.8 or newer versions. Details are explained in [Documentation: Installation](https://lisphilar.github.io/covid19-sir/INSTALLATION.html).\n\n```Bash\npip install --upgrade covsirphy\n```\n\n> **Warning**  \n> We cannot use `covsirphy` on Google Colab, which uses Python 3.7. [Binder](https://mybinder.org/) is recommended.\n\n## Demo\n\nQuickest tour of CovsirPhy is here. The following codes analyze the records in Japan.\n\n```Python\nimport covsirphy as cs\n# Data preparation,time-series segmentation, parameter estimation with SIR-F model\nsnr = cs.ODEScenario.auto_build(geo="Japan", model=cs.SIRFModel)\n# Check actual records\nsnr.simulate(name=None);\n# Show the result of time-series segmentation\nsnr.to_dynamics(name="Baseline").detect();\n# Perform simulation with estimated ODE parameter values\nsnr.simulate(name="Baseline");\n# Predict ODE parameter values (30 days from the last date of actual records)\nsnr.build_with_template(name="Predicted", template="Baseline");\nsnr.predict(days=30, name="Predicted");\n# Perform simulation with estimated and predicted ODE parameter values\nsnr.simulate(name="Predicted");\n# Add a future phase to the baseline (ODE parameters will not be changed)\nsnr.append();\n# Show created phases and ODE parameter values\nsnr.summary()\n# Compare reproduction number of scenarios (predicted/baseline)\nsnr.compare_param("Rt");\n# Compare simulated number of cases\nsnr.compare_cases("Confirmed");\n# Describe representative values\nsnr.describe()\n```\n\nOutput of `snr.simulate(name="Predicted");`\n\n<img src="https://raw.githubusercontent.com/lisphilar/covid19-sir/master/example/output/demo_jpn/04_predicted.png" width="600">\n\n## Tutorial\n\nTutorials of functionalities are included in the [CovsirPhy documentation](https://lisphilar.github.io/covid19-sir/index.html).\n\n* [Data preparation](https://lisphilar.github.io/covid19-sir/01_data_preparation.html)\n* [Data Engineering](https://lisphilar.github.io/covid19-sir/02_data_engineering.html)\n* [SIR-derived ODE models](https://lisphilar.github.io/covid19-sir/03_ode.html)\n* [Phase-dependent SIR models](https://lisphilar.github.io/covid19-sir/04_phase_dependent.html)\n* [Scenario analysis](https://lisphilar.github.io/covid19-sir/05_scenario_analysis.html)\n* [ODE parameter prediction](https://lisphilar.github.io/covid19-sir/06_prediction.html)\n\n## Release notes\n\nRelease notes are [here](https://github.com/lisphilar/covid19-sir/releases). Titles & links of issues are listed with acknowledgement.\n\nWe can see the release plan for the next stable version in [milestone page of the GitHub repository](https://github.com/lisphilar/covid19-sir/milestones). If you find a highly urgent matter, please let us know via [issue page](https://github.com/lisphilar/covid19-sir/issues).\n\n## Developers\n\nCovsirPhy library is developed by a community of volunteers. Please see the full list [here](https://github.com/lisphilar/covid19-sir/graphs/contributors).\n\nThis project started in Kaggle platform. Hirokazu Takaya ([@lisphilar](<https://www.kaggle.com/lisphilar>)) published [Kaggle Notebook: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model) on 12Feb2020 and developed it, discussing with Kaggle community. On 07May2020, "covid19-sir" repository was created. On 10May2020, `covsirphy` version 1.0.0 was published in GitHub. First release in PyPI (version 2.3.0) was on 28Jun2020.\n\n## Support\n\nPlease support this project as a developer (or a backer).\n[![Become a backer](https://opencollective.com/covsirphy/tiers/backer.svg?avatarHeight=36&width=600)](https://opencollective.com/covsirphy)\n\n## License: Apache License 2.0\n\nPlease refer to [LICENSE](https://github.com/lisphilar/covid19-sir/blob/master/LICENSE) file.\n\n## Citation\n\nPlease cite this library as follows with version number (`import covsirphy as cs; cs.__version__`).\n\n**Hirokazu Takaya and CovsirPhy Development Team (2020-2022), CovsirPhy version [version number]: Python library for COVID-19 analysis with phase-dependent SIR-derived ODE models, [https://github.com/lisphilar/covid19-sir](https://github.com/lisphilar/covid19-sir)**\n\nThis is the output of `covsirphy.__citation__`.\n\n```Python\nimport covsirphy as cs\ncs.__citation__\n```\n\n**We have no original papers the author and contributors wrote, but note that some scientific approaches, including SIR-F model, S-R change point analysis, phase-dependent approach to SIR-derived models, were developed in this project.**\n',
    'author': 'Hirokazu Takaya',
    'author_email': 'lisphilar@outlook.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lisphilar/covid19-sir/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
