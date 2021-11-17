from unittest import mock
from LTO.Transaction import Transaction
import pytest
import HandleDefault

from LTOCli.Commands import sponsorship as Spo
from LTO.Transactions.Sponsorship import Sponsorship

from LTO.Transactions.CancelSponsorship import CancelSponsorship

class TestAssociation:

    @mock.patch.object(Sponsorship, 'broadcast_to')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            Spo.func(args=['0','1'], recipient=[])
        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Spo.func(args=['test','create'],recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()

    @mock.patch.object(CancelSponsorship, 'broadcast_to')
    def testFunc2(self, mocks):
        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Spo.func(args=['test','cancel'],recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()






