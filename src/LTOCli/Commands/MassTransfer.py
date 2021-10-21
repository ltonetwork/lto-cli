from LTO.Transactions.MassTransfer import MassTransfer
from LTOCli import HandleDefault as handle
import sys
import re

def func(nameSpace, parser):
    chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
    accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''
    stdin = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
    if not stdin:
        parser.error('Type lto mass-transfer --help for instructions')
    transfers = processInput(stdin)
    transaction = MassTransfer(transfers)
    if vars(nameSpace)['unsigned'] is False:
        transaction.signWith(handle.getAccount(chainId, parser, accountName))

        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
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
