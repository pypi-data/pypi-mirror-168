# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fundamentus',
 'fundamentus.contracts',
 'fundamentus.contracts.mocks',
 'fundamentus.drivers',
 'fundamentus.drivers.interfaces',
 'fundamentus.drivers.mocks',
 'fundamentus.exceptions',
 'fundamentus.main',
 'fundamentus.stages',
 'fundamentus.stages.extraction',
 'fundamentus.stages.transformation',
 'fundamentus.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'requests-cache>=0.9.6,<0.10.0',
 'requests==2.28.1']

setup_kwargs = {
    'name': 'pyfundamentus',
    'version': '0.0.7a0',
    'description': 'Python Fundamentus is a Python API that allows you to quickly access the main fundamental indicators of the main stocks in the Brazilian market.',
    'long_description': '# Python Fundamentus\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)\n[![codecov](https://codecov.io/github/alexcamargos/pyFundamentus/branch/main/graph/badge.svg?token=44RJNBZZFQ)](https://codecov.io/github/alexcamargos/pyFundamentus)\n\n`Python Fundamentus` is a Python API that allows you to quickly access the main fundamental indicators of the main stocks in the Brazilian market.\n\n## Installation\n\n`git clone https://github.com/alexcamargos/pyFundamentus.git`\n\n`pip install -r requirements.txt`\n\n## API usage\n\n`python run_rich.py VALE3`\n\n## Examples\n\n`python run_rich.py mglu3`\n\n![](screenshot/mglu3.png)\n\n`python run_rich.py wege3`\n\n![](screenshot/wege3.png)\n\n## Autor\n\nFeito com :heart: por [Alexsander Lopes Camargos](https://github.com/alexcamargos) :wave: Entre em contato!\n\n[![GitHub](https://img.shields.io/badge/-AlexCamargos-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=github&logoColor=white&link=https://github.com/alexcamargos)](https://github.com/alexcamargos)\n[![Twitter Badge](https://img.shields.io/badge/-@alcamargos-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=twitter&logoColor=white&link=https://twitter.com/alcamargos)](https://twitter.com/alcamargos)\n[![Linkedin Badge](https://img.shields.io/badge/-alexcamargos-1ca0f1?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/alexcamargos/)](https://www.linkedin.com/in/alexcamargos/)\n[![Gmail Badge](https://img.shields.io/badge/-alcamargos@vivaldi.net-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=Gmail&logoColor=white&link=mailto:alcamargos@vivaldi.net)](mailto:alcamargos@vivaldi.net)\n\n## Copyright\n\nCopyright 2022 by Alexsander Lopes Camargos.\n\n## License\n\n[MIT License](LICENSE)\n',
    'author': 'Alexsander Lopes Camargos',
    'author_email': 'alexcamargos@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexcamargos/pyFundamentus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
