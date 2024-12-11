from lto_cli import handle_default as handle
from lto.transactions.lease import Lease
from lto.transactions.cancel_lease import CancelLease


def func_create(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']
    recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
    amount = int(name_space.amount[0] * 100000000)

    if unsigned and not no_broadcast:
        parser.error("Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto lease create --help' for more information")

    transaction = Lease(recipient=recipient, amount=amount)

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
    handle.pretty_print(transaction)


def func_cancel(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']
    lease_id = name_space.leaseId[0]

    if unsigned and not no_broadcast:
        parser.error("Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto lease cancel --help' for more information")

    transaction = CancelLease(lease_id=lease_id)

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
    handle.pretty_print(transaction)


def func_list(name_space, parser):
    action = vars(name_space)['subparser-name-lease']
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

    node = handle.get_node(chain_id, parser)
    address = handle.get_account(chain_id, parser, account_name).address
    value = node.lease_list(address)

    if action == 'out':
        items = [(x['recipient'], x['amount'] / 100000000, x['id']) for x in value if x['sender'] == address]
    else:
        items = [(x['sender'], x['amount'] / 100000000, x['id']) for x in value if x['recipient'] == address]

    if len(items) > 0:
        width = len('%d' % max(x[1] for x in items)) + 3
        for x in items:
            print(x[0], (f"%{width}.2f") % x[1], f"( {x[2]} )")
    elif action == 'out':
        print("This account is not leasing to anyone")
    else:
        print("The account is not receiving any leases")


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-lease']:
        subparser.print_help()
        return

    action = vars(name_space)['subparser-name-lease']

    if action == 'create':
        func_create(name_space, parser)
    elif action == 'cancel':
        func_cancel(name_space, parser)
    elif action in ['in', 'out']:
        func_list(name_space, parser)
    else:
        parser.error("Unknown command. Type 'lto lease --help' for more information.")
