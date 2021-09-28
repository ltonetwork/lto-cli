from LTO.Transactions.MassTransfer import MassTransfer
from LTOCli import HandleDefault as handle
import sys

def func(nameSpace, parser):

    stdin = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
    if not stdin:
        parser.error('Type lto mass-transfer --help for instructions')
    transfers = processInput(stdin)
    transaction = MassTransfer(transfers)
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())


def processInput(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = x.split(':')
        transfers.append({'recipient': recipient, 'amount': int(amount)})
    return transfers