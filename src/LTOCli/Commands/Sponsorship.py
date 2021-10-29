from LTOCli import HandleDefault as handle
from LTO.Transactions.Sponsorship import Sponsorship
from LTO.Transactions.CancelSponsorship import CancelSponsorship


def func(nameSpace,parser):
    if vars(nameSpace)['subparser-name-sponsorship']:
        chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
        accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''

    if vars(nameSpace)['subparser-name-sponsorship'] == 'create':
        transaction = Sponsorship(nameSpace.recipient[0])
        if vars(nameSpace)['unsigned'] is False:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship create --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'cancel':
        transaction = CancelSponsorship(nameSpace.recipient[0])
        if vars(nameSpace)['unsigned'] is False:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship cancel --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'list':
        pass

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'list-inbound':
        node = handle.getNode(chainId, parser)
        address = handle.getAccount(chainId, parser, accountName).address
        value = node.sponsorshipList(address)
        if value['sponsor']:
            for x in value['sponsor']:
                print(x)
        else:
            print('No inbound sponsorships found')

    else:
        parser.error('Type lto sponsorship --help for instructions')



