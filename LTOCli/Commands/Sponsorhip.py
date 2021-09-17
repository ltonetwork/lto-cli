from LTOCli import HandleDefault as handle
from LTO.Transactions.Sponsorship import Sponsorship
from LTO.Transactions.CancelSponsorship import CancelSponsorship

def func(args, recipient):
    if args[1] not in ['create', 'cancel'] and not recipient:
        raise Exception('Invalid Sponsorship syntax')

    recipient = recipient[0]

    if args[1] == 'create':
        transaction = Sponsorship(recipient)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())
    else:
        # cancel case
        transaction = CancelSponsorship(recipient)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())