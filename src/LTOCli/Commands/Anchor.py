from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor
from LTOCli import Config

def func(nameSpace, parser):
    transaction = Anchor(nameSpace.hash[0])
    transaction.signWith(handle.getAccount(parser))
    if vars(nameSpace)['unsigned'] is False:
        if vars(nameSpace)['account']:
            transaction.signWith(handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]))
        else:
            transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor --help' for more informations ")
    


