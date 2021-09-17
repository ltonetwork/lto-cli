from unittest import mock
import pytest
import os
from LTOCli import Config
import configparser
from LTO.AccountFactory import AccountFactory

class TestConfig:

    account = AccountFactory('T').create()

    def testListAccount(self):
        l, t = Config.listAccounts()
        assert l == []
        assert t == []


    def testWriteToFile(self):

        with pytest.raises(Exception):
            Config.writeToFile('L/config.ini', self.account, secName='')

        with pytest.raises(Exception):
            with mock.patch.object(Config,'nameAlreadyPresent', return_value= True):
                Config.writeToFile('L/config.ini', self.account, secName='')

    @mock.patch.object(os.path, 'exists', return_value = True)
    def testWriteToFile2(self, mocks):

        with pytest.raises(Exception):
            Config.writeToFile('L/config.ini', self.account, secName='')

        with pytest.raises(Exception):
            with mock.patch.object(Config,'nameAlreadyPresent', return_value= True):
                Config.writeToFile('L/config.ini', self.account, secName='')

    def testGetAddressFromName(self):


        with pytest.raises(Exception):
            Config.getAddressFromName('name')

        with mock.patch.object(configparser.ConfigParser, 'sections', return_value=['name']):
            with mock.patch.object(configparser.ConfigParser, 'get', return_value='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'):
                a, b = Config.getAddressFromName('name')
        assert b == 'L'
        assert a == '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'

    @mock.patch.object(configparser.ConfigParser, 'sections', return_valiue=['Default'])
    def testRemoveDefault(self, mocks):
        address = '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'
        with mock.patch.object(configparser.ConfigParser, 'get', return_value=address):
            Config.removeDefault(address)

    @mock.patch.object(configparser.ConfigParser, 'write')
    def testRemoveDefault2(self, mocks):
        with mock.patch.object(configparser.ConfigParser, 'sections', return_value=['Default']):
            with mock.patch.object(configparser.ConfigParser, 'get', return_value=['addr']):
                with mock.patch.object(configparser.ConfigParser, 'remove_section', return_value=['addr']):
                    with pytest.raises(Exception):
                        Config.removeDefault(['addr'])

    def testSetDeafultAccount(self):

        with pytest.raises(Exception):
            Config.setDefaultAccount('name')
        with pytest.raises(Exception):
            Config.setDefaultAccount('name', address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

    @mock.patch.object(os.path, 'exists', return_value=True)
    def testSetDeafultAccount2(self, mocks):
        with pytest.raises(Exception):
            Config.setDefaultAccount('name', address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        with mock.patch.object(configparser.ConfigParser, 'sections', return_value=['node']):
            with mock.patch.object(configparser.ConfigParser, 'get', return_value = 'L'):
                with pytest.raises(Exception):
                    Config.setDefaultAccount('name', address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')


    def testRemoveAccount(self):
        with pytest.raises(Exception):
            Config.removeAccount('address')

    @mock.patch.object(os.path, 'exists', return_value=True)
    def testGetNewDefault(self, mocks):
        Config.getNewDefault()
        mocks.assert_called()

    @mock.patch.object(Config, 'setDefaultAccount')
    def testGetNewDefault2(self, mocks):
        with mock.patch.object(os.path, 'exists', return_value=True):
            with mock.patch.object(configparser.ConfigParser, 'sections'):
                with mock.patch.object(configparser.ConfigParser, 'get', return_value = 'addess'):
                    Config.getNewDefault()
        mocks.assert_called()

    def testSetNode(self):
        with pytest.raises(Exception):
            Config.setnode(args=['a'], network=[])

        with pytest.raises(Exception):
            Config.setnode(args=['a', 'b'], network=[])

        with pytest.raises(Exception):
            Config.setnode(args=['a', 'b'], network=['D'])


    @mock.patch.object(configparser.ConfigParser, 'set')
    def testSetNode2(self, mocks):
        with mock.patch.object(os.path, 'exists', return_value=True):
            with mock.patch.object(configparser.ConfigParser, 'sections', return_value=['Node']):
                with pytest.raises(Exception):
                    Config.setnode(args=['a', 'b'], network=['T'])
        with mock.patch.object(os.path, 'exists', return_value=True):
            with pytest.raises(Exception):
               Config.setnode(args=['a', 'b'], network=['T'])
