from lto_cli import handle_default as handle
from lto.transactions.sponsorship import Sponsorship
from lto.transactions.cancel_sponsorship import CancelSponsorship


def func_set(name_space, parser):
    action = vars(name_space)['subparser-name-sponsorship']
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    if unsigned and not no_broadcast:
        parser.error(f"Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto sponsorship {action} --help' for more information")

    if action == 'create':
        transaction = Sponsorship(recipient)
    else:
        transaction = CancelSponsorship(recipient)

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
    handle.pretty_print(transaction)


def func_list(name_space, parser):
    if vars(name_space)['subparser-name-sponsorship'] == 'out':
        parser.error("Listing outbound sponsorships is not supported")

    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

    node = handle.get_node(chain_id, parser)
    address = handle.get_account(chain_id, parser, account_name).address
    value = node.sponsorship_list(address)

    if value['sponsor']:
        for x in value['sponsor']:
            print(x)
    else:
        print('Not sponsored')


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-sponsorship']:
        subparser.print_help()
        return
        
    if vars(name_space)['subparser-name-sponsorship'] in ['create', 'cancel']:
        func_set(name_space, parser)
    else:
        func_list(name_space, parser)
