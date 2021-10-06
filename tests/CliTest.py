import parser
from unittest import mock
from unittest.mock import patch
import pytest

from LTOCli import CLI
from LTOCli.CLI import main
from LTOCli import Config
from argparse import ArgumentParser
import argparse


class TestCLI:

    @mock.patch.object(CLI.main(), 'processArgs')
    def test(self, mocks):
        with mock.patch.object(argparse, 'ArgumentParser'):
            with mock.patch.object(Config, 'checkDirectory'):
                #with mock.patch.object(CLI.main(), 'processArgs'):
                with pytest.raises(Exception):
                    CLI.main()
        #mocks.assert_called()




'''    @mock.patch.object(argparse.ArgumentParser, 'add_argument')
    def testConstruct(self, mocks):

        with pytest.raises(Exception):
            CLI

        with mock.patch.object(CLI, 'processArgs'):
            CLI
        assert mocks.call_count == 0'''

