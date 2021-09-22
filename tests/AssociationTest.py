from unittest import mock
from LTO.Transaction import Transaction
import pytest
import HandleDefault

from LTO.Transactions.Association import Association

from LTOCli.Commands import Association  as Ass
from LTO.Transactions.RevokeAssociation import RevokeAssociation

class TestAssociation:

    @mock.patch.object(Association, 'broadcastTo')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            Ass.func(args = [], associationType=[], recipient=[], hash=[])
        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Ass.func(args=['test','issue'], associationType=[1], recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'], hash = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()

    @mock.patch.object(RevokeAssociation, 'broadcastTo')
    def testFunc2(self, mocks):
        with pytest.raises(Exception):
            Ass.func(args = [], associationType=[], recipient=[], hash=[])
        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Ass.func(args=['test','revoke'], associationType=[1], recipient = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'], hash = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()






