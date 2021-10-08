from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor


def func(nameSpace, parser):
    transaction = Anchor(nameSpace.hash[0])

    chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
    accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''

    if vars(nameSpace)['unsigned'] is False:
        transaction.signWith(handle.getAccount(chainId, parser, accountName))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor "
            "--help' for more informations ")
    handle.prettyPrint(transaction)


