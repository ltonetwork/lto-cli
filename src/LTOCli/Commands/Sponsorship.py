from LTOCli import HandleDefault as handle
from LTO.Transactions.Sponsorship import Sponsorship
from LTO.Transactions.CancelSponsorship import CancelSponsorship
from LTOCli import Config

def func(nameSpace,parser):
    if nameSpace.option[0] == 'create':
        transaction = Sponsorship(nameSpace.recipient[0])
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
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship create --help' for more informations ")
    else:
        # cancel case
        transaction = CancelSponsorship(nameSpace.recipient[0])
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
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship cancel --help' for more informations ")