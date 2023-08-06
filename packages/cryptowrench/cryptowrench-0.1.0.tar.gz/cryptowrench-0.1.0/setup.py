# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptowrench',
 'cryptowrench.validation',
 'cryptowrench.wallet',
 'cryptowrench.wallet.helpers',
 'cryptowrench.wallet.helpers.adresses']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'ecdsa>=0.18.0,<0.19.0',
 'mnemonic>=0.20,<0.21',
 'pycryptodome>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'cryptowrench',
    'version': '0.1.0',
    'description': 'A set of tools for nerding around with crypto.',
    'long_description': '# Cryptowrench\n\nThis is a set of tools that I created to play around with blockchains and cryptocurrencies in general.\n\nInstall with:\n```\npip -m install cryptowrench\n```\n\nFeel free to use it for your own projects.\n\nAlthough these tools test themselves against publicly available test vectors (which means they should be mostly correct), **please for the love of dinosaurs** do not rely on them for storing your money. Use a proper wallet for that instead (see: [ethereum.org/en/wallets/](https://ethereum.org/en/wallets), for some wallets).\n\nPlease create issues/pull requests/feature requests where needed.\n',
    'author': 'Federico Giancarelli',
    'author_email': 'hello@federicogiancarelli.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
