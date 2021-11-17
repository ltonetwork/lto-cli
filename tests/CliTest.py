import parser
from unittest import mock
from unittest.mock import patch
import pytest

from LTOCli import CLI
from LTOCli.CLI import main
from LTOCli import config
from argparse import ArgumentParser
import argparse


class TestCLI:

    @mock.patch.object(CLI.main(), 'process_args')
    def test(self, mocks):
        with mock.patch.object(argparse, 'ArgumentParser'):
            with mock.patch.object(config, 'checkDirectory'):
                #with mock.patch.object(CLI.main(), 'process_args'):
                with pytest.raises(Exception):
                    CLI.main()
        #mocks.assert_called()




'''    @mock.patch.object(argparse.ArgumentParser, 'add_argument')
    def testConstruct(self, mocks):

        with pytest.raises(Exception):
            CLI

        with mock.patch.object(CLI, 'process_args'):
            CLI
        assert mocks.call_count == 0'''

