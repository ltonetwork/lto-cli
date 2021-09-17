from unittest import mock
from LTO.Transaction import Transaction
import pytest
from LTOCli import HandleDefault
from LTO.Transactions.MassTransfer import MassTransfer
from LTOCli.Commands import MassTransfer as MasT


class TestMassTransfer:
    transfers = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj:1000000000',
                 '3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz:800000000']

    def testProcessInput(self):

        assert MasT.processInput(self.transfers) == [{'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 1000000000}, {'recipient': '3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz', 'amount': 800000000}]


    @mock.patch.object(MassTransfer, 'broadcastTo')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            MasT.func(stdin=[])

        with mock.patch.object(HandleDefault, 'getAccount', return_value = 'Account'):
            with mock.patch.object(Transaction, 'signWith'):
                MasT.func(self.transfers)
        mocks.assert_called()






