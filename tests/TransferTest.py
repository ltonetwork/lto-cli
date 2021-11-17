import configparser

from LTOCli.Commands import transfer as Tran
from unittest import mock
from LTO.Transaction import Transaction
import pytest
from LTOCli import handle_default
from LTO.Transactions.Transfer import Transfer
from argparse import ArgumentParser

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestTransfer:
    parser = ArgumentParser()

    def testFunc(self):
        nameSpace = Namespace(recipient=['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'],
                              amount=[10000000000000], account=['3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du'],
                              unsigned=False, no_broadcast=True)
        with pytest.raises(Exception):
            Tran.func()
        with mock.patch.object(handle_default, 'getDefaultAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                with mock.patch.object(handle_default, 'getAccountFromName'):
                    Tran.func(nameSpace, self.parser)

    @mock.patch.object(Transfer, 'broadcast_to')
    def testBroadcast(self, mocks):
        nameSpace = Namespace(recipient=['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'],
                              amount=[10000000000000], account=[],
                              unsigned=False, no_broadcast=False)

        with mock.patch.object(Transaction, 'signWith'):
            with mock.patch.object(handle_default, 'prettyPrint'):
                Tran.func(nameSpace, self.parser)
        mocks.assert_called()

    def testUnsignedBroadcast(self):
        nameSpace = Namespace(recipient=['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'],
                              amount=[10000000000000], account=[],
                              unsigned=True, no_broadcast=False)
        with pytest.raises(SystemExit):
            Tran.func(nameSpace, self.parser)











