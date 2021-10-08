from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer

def func(nameSpace, parser):

    recipient = nameSpace.recipient[0]
    amount = nameSpace.amount[0]
    transaction = Transfer(recipient, amount)

    chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
    accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''

    if vars(nameSpace)['unsigned'] is False:
        transaction.signWith(handle.getAccount(chainId, parser, accountName))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error("Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto transaction --help' for more informations ")
    handle.prettyPrint(transaction)