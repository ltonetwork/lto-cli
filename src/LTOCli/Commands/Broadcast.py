import json
from LTO import PyCLTO
from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer
from LTOCli import Config
import sys
from LTO.Transaction import Transaction

def func(nameSpace, parser):
    txJson = nameSpace.stdin.read() if not sys.stdin.isatty() else ""
    if not json:
        parser.error("Expected transaction as input, type 'lto broadcast --help' for instructions")

    transaction = PyCLTO().fromData(json.loads(txJson))

    if vars(nameSpace)['unsigned'] is False:
        if not transaction.proofs:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromName(vars(nameSpace)['account'][0], parser))
            else:
                transaction.signWith(handle.getDefaultAccount(parser))
        if vars(nameSpace)['no_broadcast'] is False:
            transaction = transaction.broadcastTo(handle.getNode())
    else:
        if not transaction.proofs:
            parser.error("Transaction needs to be signed before broadcasting, type 'lto broadcast --help' for instruction")
        else:
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode())

    handle.prettyPrint(transaction)


