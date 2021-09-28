from LTOCli import HandleDefault as handle
from LTO.Transactions.Lease import Lease
from LTO.Transactions.CancelLease import CancelLease

def func(nameSpace, parser):

    if vars(nameSpace)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=nameSpace.recipient[0], amount=nameSpace.amount[0])
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())
    else:
        # cancel case
        transaction = CancelLease(leaseId=nameSpace.leaseId[0])
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())