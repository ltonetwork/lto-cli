from LTOCli import HandleDefault as handle
from LTO.Transactions.Association import Association
from LTO.Transactions.RevokeAssociation import RevokeAssociation
from LTOCli import Config

def func(nameSpace, parser):
    associationType = nameSpace.type[0]
    recipient = nameSpace.recipient[0]
    hash = ''
    if nameSpace.hash:
        hash = nameSpace.hash[0]

    if nameSpace.option[0]== 'issue':
        transaction = Association(recipient=recipient, associationType=associationType, anchor=hash)
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())
    else:
        # revoke case
        transaction = RevokeAssociation(recipient=recipient, associationType=associationType, anchor=hash)
        transaction.signWith(handle.getAccount(parser))
        transaction.broadcastTo(handle.getNode())