from __future__ import annotations
from mnemonic import Mnemonic

from .helpers.adresses.bitcoin import address_P2PKH
from .helpers.adresses.ethereum import address_ethereum
from .helpers.derivation_path import derive_wallet
from .helpers.keys import get_public_key, get_private_key_and_chain_code_from_seed

class Wallet():
    def __init__(self, mnemonic: str = None, language: str = 'english', strength: int = 128, passphrase: str = '', private_key: bytes = None, chain_code: bytes = None, seed: bytes = None) -> None:
        if private_key == None and chain_code != None:
            raise Exception("If you provide a chain_code for an extended key, you need to provide a private key as well.")
        if (mnemonic != None) + (seed != None) + (private_key != None) > 1:
            raise Exception("The mnemonic, the seed and the private key/chain code are mutually exclusive. Please provide at most one of them.")
        if private_key != None and chain_code == None:
            print("You provided a private key without specifying a chain code. You won't be able to generate a hierarchical deterministic wallet.")
        if private_key != None:
            self._master_private_key = private_key
            self._master_chain_code = chain_code
            self.words = None
            self.seed = None
        else:
            if mnemonic != None:
                if len(mnemonic.split(' ')) < 12:
                    print('You are using less than 12 words to generate your wallet. This is considered unsafe and is not recommended.')
                self.words = mnemonic
                self.seed = Mnemonic.to_seed(self.words, passphrase)
            else:
                # Both the private key and the mnemonic are empty, so let's create
                # a seed based on a random mnemonic and use that to create the keys.
                available_languages = ', '.join(Mnemonic.list_languages())
                assert language in Mnemonic.list_languages(), f'Language not available. Please use one of the following: {available_languages}'
                self.words = Mnemonic(language).generate(strength)
                self.seed = Mnemonic.to_seed(self.words, passphrase)
        if self.seed != None:
            extended_private_key = get_private_key_and_chain_code_from_seed(self.seed)
            self._master_private_key = extended_private_key.private_key
            self._master_chain_code  = extended_private_key.chain_code
        
        self._master_public_key = get_public_key(self._master_private_key, compressed=True)
        self._master_uncompressed_public_key = get_public_key(self._master_private_key, compressed=False)
    
    def hd_wallet(self, path: str, compress_public_keys: bool = True, main_net: bool = True) -> Wallet:
        priv, chain, serialized_key = derive_wallet(
            derivation_path=path,
            master_private_key=self._master_private_key,
            master_chain_code=self._master_chain_code,
            flag_compress_public_keys=compress_public_keys,
            main_net=main_net)
        # print(serialized_key)
        return Wallet(private_key=priv, chain_code=chain)
    
    @property
    def address_P2PKH(self, main_net: bool = True):
        return address_P2PKH(self._master_public_key, main_net)
    
    @property
    def address_ethereum(self):
        return address_ethereum(self._master_uncompressed_public_key)
    
    @property
    def bitcoin(self):
        return _BitcoinWallet()

    @property
    def ethereum(self):
        return _EthereumWallet()


class _BitcoinWallet():
    def __init__(self, ) -> None:
        self._coin = "0'"

class _EthereumWallet():
    def __init__(self) -> None:
        self._coin = "60'"
