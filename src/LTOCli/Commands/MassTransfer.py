from LTO.Transactions.MassTransfer import MassTransfer
from LTOCli import HandleDefault as handle
import sys
import re

def func(nameSpace, parser):
    stdin = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
    if not stdin:
        parser.error('Type lto mass-transfer --help for instructions')
    transfers = processInput(stdin)
    transaction = MassTransfer(transfers)
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
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto mass-transfer --help' for more informations ")

    handle.prettyPrint(transaction)

def processInput(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = re.split('[,;:=\s]+', x)
        transfers.append({'recipient': recipient, 'amount': int(amount)})
    return transfers
