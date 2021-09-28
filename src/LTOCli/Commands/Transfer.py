from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer


def func(nameSpace):

    recipient = nameSpace.recipient[0]
    amount = nameSpace.amount[0]
    transaction = Transfer(recipient, amount)
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())
