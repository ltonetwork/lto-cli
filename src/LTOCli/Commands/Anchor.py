from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor

def func(nameSpace, parser):
    transaction = Anchor(nameSpace.hash[0])
    transaction.signWith(handle.getAccount(parser))
    transaction.broadcastTo(handle.getNode())
    


