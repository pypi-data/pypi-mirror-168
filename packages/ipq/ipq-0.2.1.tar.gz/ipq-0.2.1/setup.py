# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipq']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

extras_require = \
{'speedups': ['aiodns>=3.0.0,<4.0.0', 'cchardet>=2.1.7,<3.0.0']}

entry_points = \
{'console_scripts': ['ipq = ipq.__main__:main']}

setup_kwargs = {
    'name': 'ipq',
    'version': '0.2.1',
    'description': 'A CLI tool for gathering IP and domain name information.',
    'long_description': '# IP Query\n\nA CLI tool for gathering IP and domain name information.\n\n## Requirements\n\n- Python >= 3.7.\n- `whois` shell command.\n- `nslookup` shell command.\n- `ping` shell command.\n\n## Installation\n\nLatest stable version:\n\n```bash\npip install ipq\n```\n\nLatest stable version with speedups:\n- Adds `aiodns` and `cchardet` dependencies.\n\n```bash\npip install "ipq[speedups]"\n```\n\nDevelopment version:\n\n```bash\npip install git+https://github.com/Jonxslays/ipq.git\n```\n\n## Usage\n\n```bash\n# Check ipq version\n$ ipq -v\n$ ipq --version\n\n# Get help\n$ ipq -h\n$ ipq --help\n\n# Get info on a domain\n$ ipq google.com\n\n# Also works\n$ ipq https://google.com\n\n# Get info on an ip\n$ ipq 8.8.8.8\n\n# Ping the host\n$ ipq -p google.com\n$ ipq --ping 8.8.8.8\n\n# Get ip and whois info on a domain\n$ ipq -w google.com\n$ ipq --whois google.com\n\n# Fails: ips do not have whois info\n$ ipq -w 8.8.8.8\n```\n\n## License\n\nipq is licensed under the [MIT License](https://github.com/Jonxslays/ipq/blob/master/LICENSE).\n',
    'author': 'Jonxslays',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Jonxslays/ipq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
