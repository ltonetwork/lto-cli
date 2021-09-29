from LTOCli import HandleDefault as handle
from LTO.Transactions.Sponsorship import Sponsorship
from LTO.Transactions.CancelSponsorship import CancelSponsorship
from LTOCli import Config

def func(nameSpace,parser):
    Config.createDirectory()
    if nameSpace.option[0] == 'create':
        transaction = Sponsorship(nameSpace.recipient[0])
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())
    else:
        # cancel case
        transaction = CancelSponsorship(nameSpace.recipient[0])
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())