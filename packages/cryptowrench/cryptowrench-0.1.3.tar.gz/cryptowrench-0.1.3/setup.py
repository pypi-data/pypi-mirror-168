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
    'version': '0.1.3',
    'description': 'A set of tools for nerding around with crypto.',
    'long_description': '# Cryptowrench\n\nThis is a set of tools that I created to learn and play around with blockchains and cryptocurrencies in general.\n\nInstall with:\n```\npip -m install cryptowrench\n```\n\nFeel free to use it for your own projects.\n\n## Examples\n\n### Create a new wallet\n```python\nfrom cryptowrench.wallet import Wallet\n\n# This will create a root wallet automatically\nroot_wallet = Wallet()\n\n# Now you can show the mnemonic words generated. Store them in a safe place!\n# They will help you recover your wallet if you ever lose your computer. You can\n# also use them to import this wallet into a different wallet application.\nprint(root_wallet.words)\n\n# IMPORTANT NOTE: You should never use your root wallet to sign transactions\n# directly. Instead, you are supposed to use it to generate multiple "child\n# wallets" using the method introduced in BIP 32 (see: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).\n# These child wallets are the ones you should use for receiving and sending\n# transactions.\n\n# Enough talk! Let\'s create our first child wallet!\nchild_wallet = root_wallet.hd_wallet("m/84\'/0\'/0\'/0/0")\n\n# That\'s it :)\n\n# These are your keys (in serialized format). For details on key serialization,\n# see: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format\nprint(child_wallet.serialized_extended_private_key)\nprint(child_wallet.serialized_extended_public_key)\n\n# Now let\'s see your bitcoin address so people can send you lots of BTCs.\nprint(child_wallet.address.bitcoin.P2WPKH_wit0)\n```\n\n### Import an existing wallet (from mnemonic words)\n```python\nfrom cryptowrench.wallet import Wallet\n\n# IMPORTANT: Do not use the following words to generate your wallet because they\n# are not random and they are publicly available in the internet. If you do it,\n# you will lose all your money and axe-throwing monkeys will descend from the\n# skies to hunt you down.\nwords = \'fetch pool sight try enhance squirrel must range rotate maple resemble forest\'\n# If your wallet had a password, you should pass it to the Wallet class as well.\npwd = \'\'\n\n# This will import a root wallet from the provided mnemonic and password.\nroot_wallet = Wallet(mnemonic=words, passphrase=pwd)\n\n# This is the first child wallet.\nchild_wallet = root_wallet.hd_wallet("m/84\'/0\'/0\'/0/0")\nprint(f"P2WPKH0:  {child_wallet.address.bitcoin.P2WPKH_wit0}")\n\n# You can also generate old wallet formats, like this:\n\n# Original bitcoin wallet format (P2PKH or Pay-to-PubKey-Hash).\n# How to recognize them? They start with the number 1.\n# NOTE: it is not recommended to use this wallet format nowadays because it uses\n# the most amount of space inside a transaction and is therefore the most\n# "expensive" address type.\nchild_wallet = root_wallet.hd_wallet("m/44\'/0\'/0\'/0/0")\nprint(f"P2PKH:    {child_wallet.address.bitcoin.P2PKH}")\n\n# BIP 13 bitcoin wallet format (P2SH or Pay-to-Script-Hash).\n# How to recognize them? They start with the number 3.\n# NOTE: to better understand what these addresses enable in the bitcoin\n# blockchain, refert to the original BIP that introduced them:\n# https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki\n# Also you can take a look at BIP 16, which introduced the corresponding new\n# transaction type: https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki\nchild_wallet = root_wallet.hd_wallet("m/49\'/0\'/0\'/0/0")\nprint(f"P2SH:     {child_wallet.address.bitcoin.P2SH}")\n\n# Finally, if your seed comes from an Ethereum wallet, you can also peek into\n# those addresses as well:\nchild_wallet = root_wallet.hd_wallet("m/44\'/60\'/0\'/0/0")\nprint(f"Ethereum: {child_wallet.address.ethereum}")\n```\n\n### Import an existing wallet (from seed)\n```python\nfrom cryptowrench.wallet import Wallet\n\n# IMPORTANT: Do not use the following seed to generate your wallet because is\n# not random and it is publicly available in the internet. If you do it, you\n# will lose all your money and angry elephants will eat all your crops.\n# Make sure the seed is in bytes.\nseed = bytes.fromhex(\'000102030405060708090a0b0c0d0e0f\')\n\n# This will import a root wallet from the provided seed.\nroot_wallet = Wallet(seed=seed)\n\n# This is the first child wallet.\nchild_wallet = root_wallet.hd_wallet("m/44\'/60\'/0\'/0/0")\nprint(f"Ethereum:  {child_wallet.address.ethereum}")\n```\n\n## Disclaimer\nAlthough I try my best to make these tools as correct and reliable as possible, `please for the love of dinosaurs` do not rely on them for storing your money. Use a proper wallet for that instead (see: [ethereum.org/en/wallets/](https://ethereum.org/en/wallets) for some fully featured ones).\n\nThat said, this library has been tested against publicly available test vectors (i.e. from [bip32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Test_Vectors) and [bip39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#Test_vectors), among others), which means that it should be mostly correct for those functionalities. Expect more tests to be added in the future, and see [`run_tests.py`](https://github.com/omirete/cryptowrench/blob/master/run_tests.py) if you would like to run these tests yourself.\n\n## Colaborate :)\nPlease create issues/pull requests/feature requests where needed. I\'m also looking to collaborate in other open source projects, so let me know if you would like to talk!\n',
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
