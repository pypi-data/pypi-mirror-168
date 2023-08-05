import os

from near_api.providers import JsonProvider
from near_api.signer import Signer, KeyPair
from near_api import account

RPC_NODE = os.environ.get(
    'RPC_NODE', 'https://rpc.testnet.near.org')

# Loozr mixer information
LZR_MIXER_SECRET_KEY = os.environ.get('MIXER_SECRET_KEY')
LZR_MIXER_ACCOUNT_ID = os.environ.get(
    'MIXER_ACCOUNT_ID', default='lzr.testnet')
LZR_FACTORY_MIXER_SECRET_KEY = os.environ.get('LZR_FACTORY_MIXER_SECRET_KEY')
LZR_FACTORY_MIXER_ACCOUNT_ID = os.environ.get(
    'LZR_FACTORY_MIXER_ACCOUNT_ID', default='lzr.testnet')
LZR_TOKEN_CONTRACT_ID = os.environ.get('LZR_ACCOUNT_ID', default='lzr.testnet')


class Base:
    def __init__(self) -> None:
        self.provider = JsonProvider(RPC_NODE)
        self.lzr_mixer_signer = Signer(
            LZR_MIXER_ACCOUNT_ID,  # type: ignore
            KeyPair(LZR_MIXER_SECRET_KEY)  # type: ignore
        )
        self.lzr_mixer_account = account.Account(
            self.provider, self.lzr_mixer_signer,
            LZR_MIXER_ACCOUNT_ID)  # type: ignore


class FactoryUserAccount:
    def __init__(self) -> None:
        self.provider = JsonProvider(RPC_NODE)
        self.lzr_mixer_signer = Signer(
            LZR_FACTORY_MIXER_ACCOUNT_ID,  # type: ignore
            KeyPair(LZR_FACTORY_MIXER_SECRET_KEY)  # type: ignore
        )
        self.lzr_mixer_account = account.Account(
            self.provider, self.lzr_mixer_signer,
            LZR_FACTORY_MIXER_ACCOUNT_ID)  # type: ignore
