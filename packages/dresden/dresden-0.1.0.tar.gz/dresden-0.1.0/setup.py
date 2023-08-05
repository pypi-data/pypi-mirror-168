# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dresden']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0', 'yarl>=1.6.0']

setup_kwargs = {
    'name': 'dresden',
    'version': '0.1.0',
    'description': 'Asynchronous Python client providing Open Data information of dresden',
    'long_description': '## Python - ODP Dresden Client\n\n<!-- PROJECT SHIELDS -->\n[![GitHub Release][releases-shield]][releases]\n[![Python Versions][python-versions-shield]][pypi]\n![Project Stage][project-stage-shield]\n![Project Maintenance][maintenance-shield]\n[![License][license-shield]](LICENSE)\n\n[![GitHub Activity][commits-shield]][commits-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![GitHub Last Commit][last-commit-shield]][commits-url]\n\n[![Maintainability][maintainability-shield]][maintainability-url]\n[![Code Coverage][codecov-shield]][codecov-url]\n\n[![Build Status][build-shield]][build-url]\n[![Typing Status][typing-shield]][typing-url]\n\nAsynchronous Python client for the open datasets of Dresden (Germany).\n\n## About\n\nA python package with which you can retrieve data from the Open Data Platform of Dresden via [their API][api]. This package was initially created to only retrieve parking data from the API, but the code base is made in such a way that it is easy to extend for other datasets from the same platform.\n\n## Installation\n\n```bash\npip install dresden\n```\n\n## Datasets\n\nYou can read the following datasets with this package:\n\n- Disabled parking spaces / Parken für Menschen mit Behinderungen (476)\n\nThere are a number of parameters you can set to retrieve the data:\n\n- **limit** (default: 10) - How many results you want to retrieve.\n\n<details>\n    <summary>Click here to get more details</summary>\n\n### Disabled parking spaces\n\n| Variable | Type | Description |\n| :------- | :--- | :---------- |\n| `entry_id` | integer | The ID of the disabled parking spot |\n| `number` | integer | The number of parking spots on this location |\n| `usage_time` | string | Some locations have window times where the location is only specific for disabled parking, outside these times everyone is allowed to park there |\n| `photo` | string | URL that points to a photo that shows where the location is |\n| `created_at` | datetime | The date when this location was added to the dataset |\n| `longitude` | float | The longitude of the parking spot |\n| `latitude` | float | The latitude of the parking spot |\n\n</details>\n\n## Example\n\n```python\nimport asyncio\n\nfrom dresden import ODPDresden\n\n\nasync def main() -> None:\n    """Show example on using the Dresden API client."""\n    async with ODPDresden() as client:\n        disabled_parkings = await client.disabled_parkings()\n        print(disabled_parkings)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## Use cases\n\n[NIPKaart.nl][nipkaart]\n\nA website that provides insight into where disabled parking spaces are, based on\ndata from users and municipalities. Operates mainly in the Netherlands, but also\nhas plans to process data from abroad.\n\n## Contributing\n\nThis is an active open-source project. We are always open to people who want to\nuse the code or contribute to it.\n\nWe\'ve set up a separate document for our\n[contribution guidelines](CONTRIBUTING.md).\n\nThank you for being involved! :heart_eyes:\n\n## Setting up development environment\n\nThis Python project is fully managed using the [Poetry][poetry] dependency\nmanager.\n\nYou need at least:\n\n- Python 3.9+\n- [Poetry][poetry-install]\n\nInstall all packages, including all development requirements:\n\n```bash\npoetry install\n```\n\nPoetry creates by default an virtual environment where it installs all\nnecessary pip packages, to enter or exit the venv run the following commands:\n\n```bash\npoetry shell\nexit\n```\n\nSetup the pre-commit check, you must run this inside the virtual environment:\n\n```bash\npre-commit install\n```\n\n*Now you\'re all set to get started!*\n\nAs this repository uses the [pre-commit][pre-commit] framework, all changes\nare linted and tested with each commit. You can run all checks and tests\nmanually, using the following command:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\nTo run just the Python tests:\n\n```bash\npoetry run pytest\n```\n\n## License\n\nMIT License\n\nCopyright (c) 2022 Klaas Schoute\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n[api]: https://opendata.dresden.de\n[nipkaart]: https://www.nipkaart.nl\n\n<!-- MARKDOWN LINKS & IMAGES -->\n[build-shield]: https://github.com/klaasnicolaas/python-dresden/actions/workflows/tests.yaml/badge.svg\n[build-url]: https://github.com/klaasnicolaas/python-dresden/actions/workflows/tests.yaml\n[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-dresden.svg\n[commits-url]: https://github.com/klaasnicolaas/python-dresden/commits/main\n[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-dresden/branch/main/graph/badge.svg?token=70ZETUK1M6\n[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-dresden\n[forks-shield]: https://img.shields.io/github/forks/klaasnicolaas/python-dresden.svg\n[forks-url]: https://github.com/klaasnicolaas/python-dresden/network/members\n[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-dresden.svg\n[issues-url]: https://github.com/klaasnicolaas/python-dresden/issues\n[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-dresden.svg\n[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-dresden.svg\n[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg\n[maintainability-shield]: https://api.codeclimate.com/v1/badges/c1c6a794bf0db0086c87/maintainability\n[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-dresden/maintainability\n[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg\n[pypi]: https://pypi.org/project/dresden/\n[python-versions-shield]: https://img.shields.io/pypi/pyversions/dresden\n[typing-shield]: https://github.com/klaasnicolaas/python-dresden/actions/workflows/typing.yaml/badge.svg\n[typing-url]: https://github.com/klaasnicolaas/python-dresden/actions/workflows/typing.yaml\n[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-dresden.svg\n[releases]: https://github.com/klaasnicolaas/python-dresden/releases\n[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-dresden.svg\n[stars-url]: https://github.com/klaasnicolaas/python-dresden/stargazers\n\n[poetry-install]: https://python-poetry.org/docs/#installation\n[poetry]: https://python-poetry.org\n[pre-commit]: https://pre-commit.com\n',
    'author': 'Klaas Schoute',
    'author_email': 'hello@student-techlife.com',
    'maintainer': 'Klaas Schoute',
    'maintainer_email': 'hello@student-techlife.com',
    'url': 'https://github.com/klaasnicolaas/python-dresden',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
