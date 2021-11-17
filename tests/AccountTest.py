from LTOCli.Commands import account
from unittest import mock
import pytest
import configparser
import Config
from LTO.AccountFactory import AccountFactory

class TestAccount:

    @mock.patch.object(Config, 'writeToFile')
    def testFunc(self, mock):
        account.func(args=['0', 'create'], secName=[], network=['T'], stdin=[])
        mock.assert_called()

    @mock.patch.object(Config, 'listAccounts')
    def testFunc2(self, mock):
        account.func(args=['0', 'list'], secName=[], network=[], stdin=[])
        mock.assert_called()

    @mock.patch.object(Config, 'removeAccount')
    def testFunc3(self, mock):
        account.func(args=['0', 'remove', 'ewrwer'], secName=[], network=[], stdin=[])
        mock.assert_called()

    @mock.patch.object(Config, 'setDefaultAccount')
    def testFunc4(self, mock):
        account.func(args=['0', 'set-default', ['errere']], secName=[], network=[], stdin=[])
        mock.assert_called()

    @mock.patch.object(configparser.ConfigParser, 'write')
    def testFunc5(self, mocks):
        with mock.patch.object(AccountFactory, 'createFromSeed', return_value = 'account'):
            with pytest.raises(Exception):
                account.func(args=['0', 'seed'], secName=[], network=[], stdin=['12'])
        #mocks.assert_called()


