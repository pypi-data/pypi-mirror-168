# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptowrench',
 'cryptowrench.wallet',
 'cryptowrench.wallet.helpers',
 'cryptowrench.wallet.helpers.adresses']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'bech32>=1.2.0,<2.0.0',
 'ecdsa>=0.18.0,<0.19.0',
 'mnemonic>=0.20,<0.21',
 'pycryptodome>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'cryptowrench',
    'version': '0.1.2',
    'description': 'A set of tools for nerding around with crypto.',
    'long_description': "# Cryptowrench\n\nThis is a set of tools that I created to learn and play around with blockchains and cryptocurrencies in general.\n\nInstall with:\n```\npip -m install cryptowrench\n```\n\nFeel free to use it for your own projects.\n\n## Disclaimer\nAlthough I try my best to make these tools as correct and reliable as possible, `please for the love of dinosaurs` do not rely on them for storing your money. Use a proper wallet for that instead (see: [ethereum.org/en/wallets/](https://ethereum.org/en/wallets), for some wallets).\n\nThat said, this library has been tested against publicly available test vectors (i.e. from [bip32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Test_Vectors) and [bip39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#Test_vectors), among others), which means that it should be mostly correct for those functionalities. Expect more tests to be added in the future, and see [`run_tests.py`](https://github.com/omirete/cryptowrench/blob/master/run_tests.py) if you would like to run these tests yourself.\n\n## Colaborate :)\nPlease create issues/pull requests/feature requests where needed. I'm also looking to collaborate in other open source projects, so let me know if you would like to talk!\n",
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
