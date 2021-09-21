from unittest import mock
import pytest
from LTOCli import CLI
import argparse


class TestCLI:

    @mock.patch.object(argparse.ArgumentParser, 'add_argument')
    def testConstruct(self, mocks):

        with pytest.raises(Exception):
            CLI

        '''with mock.patch.object(CLI, 'processArgs'):
            CLI
        assert mocks.call_count == 0'''

