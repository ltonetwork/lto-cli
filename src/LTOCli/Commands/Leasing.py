from LTOCli import HandleDefault as handle
from LTO.Transactions.Lease import Lease
from LTO.Transactions.CancelLease import CancelLease


def func(nameSpace, parser):
    if vars(nameSpace)['subparser-name-lease']:
        chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
        accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''

    if vars(nameSpace)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=nameSpace.recipient[0], amount=nameSpace.amount[0])
        if vars(nameSpace)['unsigned'] is False:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease create --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-lease'] == 'cancel':
        transaction = CancelLease(leaseId=nameSpace.leaseId[0])
        if vars(nameSpace)['unsigned'] is False:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease cancel --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-lease'] == 'list':  # The lease that I'm giving
        node = handle.getNode(chainId, parser)
        address = handle.getAccount(chainId, parser, accountName).address
        value = node.leaseList(address)
        flag = 0
        for x in value:
            if x['sender'] == address:  # outbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No outbound lease found")

    elif vars(nameSpace)['subparser-name-lease'] == 'list-inbound':  # The lease that I've received
        node = handle.getNode(chainId, parser)
        address = handle.getAccount(chainId, parser, accountName).address
        value = node.leaseList(address)
        flag = 0
        for x in value:
            if x['recipient'] == address:  # inbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No inbound lease found")

    else:
        parser.error('Type lto lease --help for instructions')
