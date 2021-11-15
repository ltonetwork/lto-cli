import pytest
from LTOCli import handle_default as handle
from unittest import mock
from LTOCli import config
from pathlib import Path
from LTO.AccountFactory import AccountFactory
from configparser import ConfigParser
import os
from LTO.PublicNode import PublicNode

class TestHandleDefault:
    parser = ConfigParser()

    #assert HandleDefault.URL == 'https://nodes.lto.network'

    assert handle.path == Path.joinpath(Path.home(), 'lto')

    @mock.patch.object(handle, 'prettyPrint')
    def testPrettyPrint(self, mocks):
        handle.prettyPrint('test')
        mocks.assert_called()

    @mock.patch.object(AccountFactory, 'createFromSeed')
    def testGetAccountFromName(self, mocks):
        with mock.patch.object(config, 'findAccount'):
            handle.getAccountFromName('name', 'parser')
        mocks.assert_called()

    @mock.patch.object(config, 'findAccount', return_value = False)
    def testGetAccountFromNameFail(self, mocks):
        with pytest.raises(Exception):
            handle.getAccountFromName('name', 'parser')
        mocks.assert_called()

    def testGetDefaultAccountNoDefault(self):
        with pytest.raises(Exception):
            handle.getDefaultAccount(self.parser)

    @mock.patch.object(AccountFactory, 'createFromSeed', return_value = 1)
    def testGetDefaultAccount(self, mocks):
        with mock.patch.object(os, 'path', return_value = True):
            with mock.patch.object(ConfigParser, 'read'):
                with mock.patch.object(ConfigParser, 'sections', return_value = ['Default']):
                    with mock.patch.object(ConfigParser, 'get', return_value = 1):
                        with mock.patch.object(config, 'findAccount', return_value = [True, 3]):
                            with pytest.raises(Exception):
                                handle.getDefaultAccount(self.parser)

    def testGetNode(self):
        with mock.patch.object(os, 'path', return_value = False):
            node = handle.getNode()
            assert isinstance(node, PublicNode)





