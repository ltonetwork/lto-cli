from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer
from LTOCli import Config

def func(nameSpace, parser):
    recipient = nameSpace.recipient[0]
    amount = nameSpace.amount[0]
    transaction = Transfer(recipient, amount)

    if vars(nameSpace)['unsigned'] is False:
        if vars(nameSpace)['account']:
            transaction.signWith(handle.getAccountFromOption(parser, nameSpace['account'][0]))
        else:
            transaction.signWith(handle.getAccount(parser))

        if vars(nameSpace)['no_broadcast'] is False:
            transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error("Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto transaction --help' for more informations ")


