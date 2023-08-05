import json

from near_api.signer import Signer, KeyPair
from near_api.account import Account
from near_api.providers import JsonProvider
from loozr_near_sdk.utils.base import RPC_NODE
from loozr_near_sdk.utils.constants import (
    CONTRACT_ATTACHED_GAS, CONTRACT_INITIAL_BALANCE)
from loozr_near_sdk.utils.base import FactoryUserAccount, LZR_FACTORY_MIXER_SECRET_KEY, LZR_FACTORY_MIXER_ACCOUNT_ID
from loozr_near_sdk.account import AccountHelper


def get_creator_account_id_from_name(account_name):
    return "%s.%s" % (account_name, LZR_FACTORY_MIXER_ACCOUNT_ID)


class CreatorCoinAccount:
    def __init__(self, account_id: str) -> None:
        self.provider = JsonProvider(RPC_NODE)
        self.lzr_mixer_signer = Signer(
            account_id,  # type: ignore
            KeyPair(LZR_FACTORY_MIXER_SECRET_KEY)  # type: ignore
        )
        self.lzr_mixer_account = Account(
            self.provider, self.lzr_mixer_signer,
            account_id)  # type: ignore


class CreatorCoin:
    def __init__(self, account_provider=None) -> None:
        if account_provider is None:
            account_provider = FactoryUserAccount()
        self.account = account_provider

    def create_coin(self, account_id: str):
        """Takes `account_id` is without the domain, eg:
        instead of `myname.near` account_id == `myname` and
        deploy a creator coin on the account.

        `account_id` should be non-existent at the time
        of making this call since the factory contract
        will create the account before deploying the contract.

        Args:
            account_id (str): the account name of the contract to deploy
        """
        contract_id = self.account.lzr_mixer_account.account_id
        method = 'create'
        args = {"owner_id": contract_id, "name": account_id}

        res = self.account.lzr_mixer_account.function_call(
            contract_id,
            method,
            args,  # type: ignore
            gas=CONTRACT_ATTACHED_GAS,
            amount=CONTRACT_INITIAL_BALANCE)  # type: ignore
        return res

    def buy_token(self, account_id: str, amount: int, contract_id: str):
        """Sends loozr to creator coin contract in exchange for creator coin.

        `amount` is first transferred from `account_id` to the
        creator coin contract before calling the minting function.
        This is to make sure there is always loozr in the reserve to
        compute the bonding curve functions

        Args:
            account_id (str): Account that receives the creator coin
            amount (int): Amount in loozr to send in exchange for creator coin
        """
        method = 'ft_mint'
        args = {"account_id": account_id, "amount": str(amount)}

        account_helper_provider = AccountHelper()
        account_helper_provider.transfer_from(
            account_id, contract_id, str(amount))  # type: ignore
        
        creator_coin_account = CreatorCoinAccount(contract_id)

        res = creator_coin_account.lzr_mixer_account.function_call(
            contract_id, method, args)  # type: ignore
        return res

    def sell_token(self, account_id: str, amount: int, contract_id: str):
        method = 'ft_burn'
        args = {"account_id": account_id, "amount": str(amount)}

        creator_coin_account = CreatorCoinAccount(contract_id)
        res = creator_coin_account.lzr_mixer_account.function_call(
            contract_id, method, args)  # type: ignore
        return res

    def reserve_balance(self, contract_id: str):
        res = self.account.provider.view_call(
            contract_id, 'reserve_balance', json.dumps({}).encode('utf8'))
        balance = json.loads("".join(map(chr, res['result'])))
        return balance

    def total_supply(self, contract_id: str):
        res = self.account.provider.view_call(
            contract_id, 'ft_total_supply', json.dumps({}).encode('utf8'))
        balance = json.loads("".join(map(chr, res['result'])))
        return balance

    def balance_of(self, account_id: str, contract_id: str):
        res = self.account.provider.view_call(
            contract_id, 'ft_balance_of', json.dumps({"account_id": account_id}).encode('utf8'))
        balance = json.loads("".join(map(chr, res['result'])))
        return balance
