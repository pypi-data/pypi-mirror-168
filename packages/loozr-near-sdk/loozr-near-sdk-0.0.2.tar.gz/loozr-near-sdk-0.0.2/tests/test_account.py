import unittest

from loozr_near_sdk.account import AccountHelper
from loozr_near_sdk.utils.constants import ACCOUNT_INIT_BALANCE
from loozr_near_sdk.utils.base import LZR_MIXER_ACCOUNT_ID


class AccountHelperTest(unittest.TestCase):
    def setUp(self):
        self.account_helper = AccountHelper()

    def test_check_account(self):
        account_id = self.account_helper.get_new_id_from_name('test_user1')
        account_id_name = account_id.split('-')[0]

        self.assertEqual(account_id_name, 'test_user1')

        new_account = self.account_helper.create_account(
            account_id)
        self.assertEqual(new_account[0].state['amount'],
                         str(ACCOUNT_INIT_BALANCE))

    def test_account_id_by_name(self) -> None:
        account_name = 'test_user'
        account_id = self.account_helper.get_account_id_from_name(account_name)
        self.assertEqual(account_id, f'test_user.{LZR_MIXER_ACCOUNT_ID}')
