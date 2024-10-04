from lto_cli import handle_default as handle
from lto.transactions.association import Association
from lto.transactions.revoke_association import RevokeAssociation
import json
from lto.crypto import decode


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-association']:
        subparser.print_help()
        return
        
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    node = handle.get_node(chain_id, parser)

    if vars(name_space)['subparser-name-association'] in ['issue','revoke']:
        sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
        association_type = name_space.type[0]
        recipient = name_space.recipient[0] if node.validate_address(name_space.recipient[0]) else handle.get_account(chain_id, parser, name_space.recipient[0]).address

        subject = ''
        if name_space.subject:
            subject = name_space.subject[0]
        if vars(name_space)['subparser-name-association'] == 'issue':
            transaction = Association(recipient=recipient, association_type=association_type, subject=decode(subject, "hex"))
            if vars(name_space)['unsigned'] is False:
                transaction.sign_with(handle.get_account(chain_id, parser, account_name))
                if sponsor:
                    transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
                if vars(name_space)['no_broadcast'] is False:
                    transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
            elif vars(name_space)['no_broadcast'] is False:
                parser.error(
                    "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association issue --help' for more informations ")
        else:  # revoke case
            transaction = RevokeAssociation(recipient=recipient, association_type=association_type, subject=decode(subject, "hex"))
            if vars(name_space)['unsigned'] is False:
                if vars(name_space)['account']:
                    transaction.sign_with(handle.get_account(chain_id, parser, account_name))
                    if sponsor:
                        transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
                if vars(name_space)['no_broadcast'] is False:
                    transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
            elif vars(name_space)['no_broadcast'] is False:
                parser.error(
                    "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto association revoke --help' for more informations ")
        handle.pretty_print(transaction)
    else:
        node = handle.get_node(chain_id, parser)
        account = handle.get_account(chain_id, parser, account_name)

        if vars(name_space)['subparser-name-association'] == 'in':
            list = node.association_list(account.address)['incoming']
            for association in list:
                print(json.dumps(association, indent=2))
        else:
            list = node.association_list(account.address)['outgoing']
            for association in list:
                print(json.dumps(association, indent=2))

