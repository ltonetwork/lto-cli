import json
from LTO import PyCLTO
from LTOCli import HandleDefault as handle
import sys

def func(nameSpace, parser):
    chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
    accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''
    txJson = nameSpace.stdin.read() if not sys.stdin.isatty() else ""
    if not json:
        parser.error("Expected transaction as input, type 'lto broadcast --help' for instructions")

    transaction = PyCLTO().fromData(json.loads(txJson))

    if vars(nameSpace)['unsigned'] is False:
        if not transaction.proofs:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
    else:
        if not transaction.proofs:
            parser.error("Transaction needs to be signed before broadcasting, type 'lto broadcast --help' for instruction")
        else:
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))

    handle.prettyPrint(transaction)


