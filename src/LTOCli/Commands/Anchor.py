from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor
from LTOCli import Config

def func(nameSpace, parser):
    Config.createDirectory()
    transaction = Anchor(nameSpace.hash[0])
    transaction.signWith(handle.getAccount(parser))
    transaction.broadcastTo(handle.getNode())
    


