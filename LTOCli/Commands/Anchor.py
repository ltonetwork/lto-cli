from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor

def func(hash):
    if not hash:
        raise Exception('No hash was passed')

    hash = hash[0]

    transaction = Anchor(hash)
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())


