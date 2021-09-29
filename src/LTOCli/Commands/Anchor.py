from LTOCli import HandleDefault as handle
from LTO.Transactions.Anchor import Anchor
from LTOCli import Config

def func(nameSpace, parser):
    transaction = Anchor(nameSpace.hash[0])
    transaction.signWith(handle.getAccount(parser))
    if vars(nameSpace)['no_broadcast'] == False:
        transaction.broadcastTo(handle.getNode())
    


