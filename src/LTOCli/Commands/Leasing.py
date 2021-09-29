from LTOCli import HandleDefault as handle
from LTO.Transactions.Lease import Lease
from LTO.Transactions.CancelLease import CancelLease
from LTOCli import Config

def func(nameSpace, parser):
    Config.createDirectory()
    if vars(nameSpace)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=nameSpace.recipient[0], amount=nameSpace.amount[0])
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['subparser-name-lease'] == 'cancel':
        transaction = CancelLease(leaseId=nameSpace.leaseId[0])
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())
    else:
        parser.error('Type lto lease --help for instructions')