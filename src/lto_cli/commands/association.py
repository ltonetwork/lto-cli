from lto_cli import handle_default as handle
from lto.transactions.association import Association
from lto.transactions.revoke_association import RevokeAssociation
import json
from lto.crypto import decode


def set_func(name_space, parser):
    action = vars(name_space)['subparser-name-association']
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    association_type = name_space.type[0]
    recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    if unsigned and not no_broadcast:
        parser.error(
            f"Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto association {action} --help' for more information")

    subject = ''
    if name_space.subject:
        subject = name_space.subject[0]

    if action == 'issue':
        transaction = Association(recipient=recipient, association_type=association_type, subject=decode(subject, "hex"))
    else:
        transaction = RevokeAssociation(recipient=recipient, association_type=association_type,
                                        subject=decode(subject, "hex"))

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
    handle.pretty_print(transaction)


def list_func(name_space, parser):
    action = vars(name_space)['subparser-name-association']
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    node = handle.get_node(chain_id, parser)
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    account = handle.get_account(chain_id, parser, account_name)

    if action == 'in':
        list = node.association_list(account.address)['incoming']
    else:
        list = node.association_list(account.address)['outgoing']

    for association in list:
        print(json.dumps(association, indent=2))


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-association']:
        subparser.print_help()
        return
        
    if vars(name_space)['subparser-name-association'] in ['issue', 'revoke']:
        set_func(name_space, parser)
    else:
        list_func(name_space, parser)
