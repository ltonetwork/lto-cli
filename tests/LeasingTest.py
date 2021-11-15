from unittest import mock
from LTO.Transaction import Transaction
import pytest
import HandleDefault

from LTOCli.Commands import leasing as Leasing
from LTO.Transactions.Lease import Lease

from LTO.Transactions.CancelLease import CancelLease

class TestLeasing:

    @mock.patch.object(Lease, 'broadcastTo')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            Leasing.func(args = ['0', '1'], recipient=[], amount=[], leaseId=[])

        with pytest.raises(Exception):
            Leasing.func(args = ['0', 'create'], recipient=[], amount=[], leaseId=[])

        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Leasing.func(args=['0', 'create'], recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'], amount = [1000], leaseId = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()

    @mock.patch.object(CancelLease, 'broadcastTo')
    def testFunc2(self, mocks):
        with pytest.raises(Exception):
            Leasing.func(args = ['0', 'cancel'], recipient=[], amount=[], leaseId=[])

        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Leasing.func(args=['0', 'cancel'], recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'], amount = [1000], leaseId = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()






