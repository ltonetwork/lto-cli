from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor

def func(nameSpace):
    print(nameSpace)
    transaction = Anchor(nameSpace.hash[0])
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())


