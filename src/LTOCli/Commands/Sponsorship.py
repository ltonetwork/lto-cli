from LTOCli import HandleDefault as handle
from LTO.Transactions.Sponsorship import Sponsorship
from LTO.Transactions.CancelSponsorship import CancelSponsorship
from LTOCli import Config
from LTO.PublicNode import PublicNode

def func(nameSpace,parser):
    if vars(nameSpace)['subparser-name-sponsorship'] == 'create':
        transaction = Sponsorship(nameSpace.recipient[0])
        transaction.signWith(handle.getDefaultAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromName(vars(nameSpace)['account'][0], parser))
            else:
                transaction.signWith(handle.getDefaultAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship create --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'cancel':
        transaction = CancelSponsorship(nameSpace.recipient[0])
        transaction.signWith(handle.getDefaultAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromName(vars(nameSpace)['account'][0], parser))
            else:
                transaction.signWith(handle.getDefaultAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship cancel --help' for more informations ")
        handle.prettyPrint(transaction)

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'list':
        pass

    elif vars(nameSpace)['subparser-name-sponsorship'] == 'list-inbound':
        node = handle.getNode()
        if vars(nameSpace)['account']:
            address = handle.getAccountFromName(vars(nameSpace)['account'][0], parser).address
        else:
            address = handle.getDefaultAccount(parser).address
        value = node.sponsorshipList(address)
        if value['sponsor']:
            for x in value['sponsor']:
                print(x)
        else:
            print('No inbound sponsorships found')

    else:
        parser.error('Type lto sponsorship --help for instructions')



