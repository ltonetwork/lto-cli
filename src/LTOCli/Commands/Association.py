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
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, nameSpace['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association issue --help' for more informations ")
    else:
        # revoke case
        transaction = RevokeAssociation(recipient=recipient, associationType=associationType, anchor=hash)
        transaction.signWith(handle.getAccount(parser))
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccountFromOption(parser, nameSpace['account'][0]))
            else:
                transaction.signWith(handle.getAccount(parser))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction.broadcastTo(handle.getNode())
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association revoke --help' for more informations ")