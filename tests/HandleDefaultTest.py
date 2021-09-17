import configparser

import pytest
from configparser import ConfigParser
from LTOCli import HandleDefault
from unittest import mock
from LTOCli import Config
from LTO.PublicNode import PublicNode


class TestHandleDefault:

    assert HandleDefault.URL == 'https://nodes.lto.network'
    assert HandleDefault.CHAIN_ID == 'L'

    def testGetNode(self):
        node = HandleDefault.getNode()
        assert node.url == 'https://nodes.lto.network'

        with mock.patch.object(configparser.ConfigParser, 'sections', return_value=['Node']):
            with mock.patch.object(configparser.ConfigParser, 'get', return_value='https://nodes.lto.network'):
                node = HandleDefault.getNode()
        assert node.url == 'https://nodes.lto.network'

    def testGetAccount(self):
        with pytest.raises(Exception):
            HandleDefault.getAccount()

    @mock.patch.object(ConfigParser, 'sections', return_value=['Default'])
    def testGetAccount2(self, mocks):
        with mock.patch.object(ConfigParser, 'get', return_value='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'):
            HandleDefault.getAccount()

    @mock.patch.object(Config, 'findAccountSection', return_value='')
    def testGetSeedFromAddress(self, mock):
        with pytest.raises(Exception):
            HandleDefault.getSeedFromAddress('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

