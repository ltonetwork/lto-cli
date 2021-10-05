import json

from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer
from LTOCli import Config
import sys
from LTO.Transaction import Transaction

def func(nameSpace, parser):

    txJson = nameSpace.stdin.read() if not sys.stdin.isatty() else ""
    if not json:
        parser.error("Expected transaction as input, type 'lto broadcast --help' for instructions")

    transaction = Transaction.fromData(json.loads(txJson))

    if not transaction.proofs:
        if vars(nameSpace)['account']:
            transaction.signWith(handle.getAccountFromOption(parser, vars(nameSpace)['account'][0]))
        else:
            transaction.signWith(handle.getAccount(parser))

    #transaction.broadcastTo(handle.getNode())


