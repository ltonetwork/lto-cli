from LTOCli import HandleDefault as handle
from LTO.Transactions.Lease import Lease
from LTO.Transactions.CancelLease import CancelLease
from LTOCli import Config

def func(nameSpace, parser):


    if vars(nameSpace)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=nameSpace.recipient[0], amount=nameSpace.amount[0])
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, nameSpace['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease create --help' for more informations ")
    elif vars(nameSpace)['subparser-name-lease'] == 'cancel':
        transaction = CancelLease(leaseId=nameSpace.leaseId[0])
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, nameSpace['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease cancel --help' for more informations ")
    else:
        parser.error('Type lto lease --help for instructions')