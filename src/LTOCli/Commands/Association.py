from LTOCli import HandleDefault as handle
from LTO.Transactions.Association import Association
from LTO.Transactions.RevokeAssociation import RevokeAssociation


def func(nameSpace, parser):
    associationType = nameSpace.type[0]
    recipient = nameSpace.recipient[0]
    hash = ''
    if nameSpace.hash:
        hash = nameSpace.hash[0]

    chainId = handle.check(nameSpace.network[0], parser) if nameSpace.network else 'L'
    accountName = vars(nameSpace)['account'][0] if vars(nameSpace)['account'] else ''

    if nameSpace.option[0]== 'issue':
        transaction = Association(recipient=recipient, associationType=associationType, anchor=hash)
        if vars(nameSpace)['unsigned'] is False:
            transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association issue --help' for more informations ")
    else:
        # revoke case
        transaction = RevokeAssociation(recipient=recipient, associationType=associationType, anchor=hash)
        if vars(nameSpace)['unsigned'] is False:
            if vars(nameSpace)['account']:
                transaction.signWith(handle.getAccount(chainId, parser, accountName))
            if vars(nameSpace)['no_broadcast'] is False:
                transaction = transaction.broadcastTo(handle.getNode(chainId, parser))
        elif vars(nameSpace)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association revoke --help' for more informations ")

    handle.prettyPrint(transaction)