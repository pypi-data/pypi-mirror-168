import time
import os

from loozr_near_sdk.utils.base import (
    Base, LZR_MIXER_SECRET_KEY,
    LZR_MIXER_ACCOUNT_ID,
    RPC_NODE,
    LZR_TOKEN_CONTRACT_ID)
from near_api.account import Account, TransactionError
from near_api.providers import JsonProvider
from near_api.signer import Signer, KeyPair

from loozr_near_sdk.utils.constants import ACCOUNT_INIT_BALANCE


class AccountHelper():
    def __init__(self, account_provider=None) -> None:
        if account_provider is None:
            account_provider = Base()
        self.provider = account_provider.provider
        self.lzr_mixer_signer = account_provider.lzr_mixer_signer
        self.lzr_mixer_account = account_provider.lzr_mixer_account

    def check_account(self, account_id):
        """Gets account details of `account_id` from
        the near blockchain or throw a JsonProviderError
        if account does not exist"""
        res = self.provider.get_account(account_id)
        return res

    def get_account_details(self, account_id):
        return self.provider.get_account(account_id)

    def get_account_id_from_name(self, account_name):
        return "%s.%s" % (account_name, LZR_MIXER_ACCOUNT_ID)

    def get_new_id_from_name(self, account_name):
        return "%s-%s.%s" % (account_name, int(
            time.time() * 10_000), LZR_MIXER_ACCOUNT_ID)

    def create_account(self, account_id, amount=ACCOUNT_INIT_BALANCE):
        res = self.lzr_mixer_account.create_account(
            account_id, self.lzr_mixer_account.signer.public_key, amount)
        signer = Signer(
            account_id, self.lzr_mixer_account.signer.key_pair)
        account = Account(
            self.lzr_mixer_account.provider, signer, account_id)
        return account, res

    def transfer_from(
            self, account_id: str,
            to: str, amount: int | str,
            contract_id=LZR_TOKEN_CONTRACT_ID):
        provider = JsonProvider(RPC_NODE)
        signer = Signer(account_id, KeyPair(
            LZR_MIXER_SECRET_KEY))  # type: ignore
        account = Account(provider, signer, account_id)
        account.function_call(
            contract_id, 'ft_transfer',
            {"receiver_id": to, "amount": str(amount)},  # type: ignore
            amount=1)

    def create_another_if_exist(self, account_name: str, amount=10 ** 24):
        account_id = self.get_account_id_from_name(
            account_name)
        try:
            if self.get_account_details(account_id):
                account_id = self.get_new_id_from_name(account_name)
                return self.create_account(account_id, amount)
        except TransactionError:
            return self.create_account(account_id, amount)
