from unittest import mock
from LTO.Transaction import Transaction
import pytest
import HandleDefault

from LTOCli.Commands import anchor as Anch
from LTO.Transactions.Anchor import Anchor

class TestAnchor:

    @mock.patch.object(Anchor, 'broadcast_to')
    def testFunc(self, mocks):
        with pytest.raises(Exception):
            Anch.func(hash=[])
        with mock.patch.object(HandleDefault, 'getAccount', return_value ='Account'):
            with mock.patch.object(Transaction, 'signWith'):
                Anch.func(['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'])
        mocks.assert_called()






