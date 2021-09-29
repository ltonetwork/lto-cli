from LTOCli import HandleDefault as handle
from LTO.Transactions.Transfer import Transfer
from LTOCli import Config

def func(nameSpace, parser):
    Config.createDirectory()
    recipient = nameSpace.recipient[0]
    amount = nameSpace.amount[0]
    transaction = Transfer(recipient, amount)
    transaction.signWith(handle.getAccount(parser))
    transaction.broadcastTo(handle.getNode())
