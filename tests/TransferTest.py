from LTOCli.Commands import Transfer as Tran
from unittest import mock
from LTO.Transaction import Transaction
import pytest
from LTOCli import HandleDefault
from LTO.Transactions.Transfer import Transfer

class TestTransfer:

    @mock.patch.object(Transfer, 'broadcastTo')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            Tran.func(recipient=[], amount=[])
        with mock.patch.object(HandleDefault, 'getAccount', return_value = 'Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Tran.func(['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'], [10000000000000])
        mocks.assert_called()






