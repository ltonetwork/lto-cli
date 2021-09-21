from LTO.Transactions.MassTransfer import MassTransfer
from LTOCli import HandleDefault as handle


def func(stdin):
    if stdin == []:
        raise Exception("Transfers not present")

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