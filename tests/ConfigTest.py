from unittest import mock
import pytest
import os
from LTOCli import Config
from LTO.AccountFactory import AccountFactory
from configparser import ConfigParser
from pathlib import Path
import builtins
import configparser

class TestConfig:
    assert Config.CHAIN_ID == 'L'
    assert Config.path == Path.joinpath(Path.home(), 'lto')

    @mock.patch.object(ConfigParser, 'sections', return_value = 'True')
    def testWriteToFile(self, mocks):
        with mock.patch.object(os, 'path', return_value = True):
            with mock.patch.object(ConfigParser, 'read', return_value=True):
                with mock.patch.object(Config, 'findAccount', return_value=False):
                    with mock.patch.object(ConfigParser, 'set', return_value=True):
                        with mock.patch.object(ConfigParser, 'add_section'):
                            with pytest.raises(Exception):
                                Config.writeToFile('chainId', 'Account', 'secName', 'parser')


    def testFindAccountNotFound(self):
        with mock.patch.object(builtins, 'next', return_value = ['ds','sdf','sdfd']):
            assert Config.findAccount() == False

    def testFindAccountFound(self):
        with mock.patch.object(builtins, 'next', return_value = ['ds','sdf','Accounts.ini']):
            assert Config.findAccount() == False

    def testFindAccountInConfig(self):
        with mock.patch.object(configparser.RawConfigParser, 'sections', return_value = ['dsfds', ['fdsfsdf']]):
            with mock.patch.object(configparser.RawConfigParser, 'get', return_value = 'test'):
                assert Config.findAccountInConfig(config=configparser.RawConfigParser) == False