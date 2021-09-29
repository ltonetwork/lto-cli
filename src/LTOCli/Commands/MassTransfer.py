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
    transaction.signWith(handle.getAccount(parser))
    if vars(nameSpace)['unsigned'] is False:
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction.broadcastTo(handle.getNode())
    elif vars(nameSpace)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto mass-transfer --help' for more informations ")



def processInput(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = re.split('[,;:=\s]+', x)
        transfers.append({'recipient': recipient, 'amount': int(amount)})
    return transfers
