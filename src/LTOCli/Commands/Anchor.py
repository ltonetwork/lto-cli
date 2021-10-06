from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor
from LTOCli import Config
import json
def func(nameSpace, parser):
    transaction = Anchor(nameSpace.hash[0])

    if vars(nameSpace)['unsigned'] is False:
        if vars(nameSpace)['account']:
            transaction.signWith(handle.getAccountFromName(vars(nameSpace)['account'][0], parser))
        else:
            transaction.signWith(handle.getDefaultAccount(parser))

        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor --help' for more informations ")
    handle.prettyPrint(transaction)


