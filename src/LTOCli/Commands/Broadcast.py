from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer
from LTOCli import Config
import sys

def func(nameSpace, parser):

    print(nameSpace)
    tx = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
    if not tx:
        parser.error("Expected transaction as input, type 'lto broadcast --help' for instructions")

    '''recipient = nameSpace.recipient[0]
    amount = nameSpace.amount[0]
    transaction = Transfer(recipient, amount)

    if vars(nameSpace)['unsigned'] is False:
        if vars(nameSpace)['account']:
            transaction.signWith(handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]))
        else:
            transaction.signWith(handle.getAccount(parser))

        if vars(nameSpace)['no_broadcast'] is False:
            transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error("Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto transaction --help' for more informations ")'''


