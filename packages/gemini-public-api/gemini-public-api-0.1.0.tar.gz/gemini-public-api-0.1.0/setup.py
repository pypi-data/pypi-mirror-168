# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gemini_public_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gemini-public-api',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Gemini Public API \n\nA Python wrapper for the public Gemini API.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine.\n\n### Installing\nInstall package through pip\n```\npip3 install gemini-public-api\n```\n\nAlternatively, clone the repo\n\n```\ngit clone https://github.com/michalpolit/gemini-public-api.git\n```\n\nand install dependencies\n\n```\npoetry install\n```\n\n\n## Running the tests\nIn order to run tests, dependencies must be installed using\n```\npoetry install --with test\n```\n\nTo run the tests\n\n```\ncoverage run -m pytest\n```\n\nTo show test coverage\n\n```\ncoverage report -m\n```\n\n## Usage\n\n```python\nfrom gemini_public_api.api import GeminiPublicAPI\n\nsymbols = GeminiPublicAPI.get_symbols()\nprint(symbols)\n```\n\n## Built With\n\n* [Poetry](https://python-poetry.org/docs/) - Packaging and dependency management\n* [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) - Property-based testing\n\n## Authors\n\n* **Michal Polit**\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
