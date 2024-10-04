from lto_cli import handle_default as handle
from lto.transactions.lease import Lease
from lto.transactions.cancel_lease import CancelLease


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-lease']:
        subparser.print_help()
        return
    
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

    if vars(name_space)['subparser-name-lease'] == 'create':
        recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
        sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
        transaction = Lease(recipient=recipient, amount=int(name_space.amount[0] * 100000000))
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease create --help' for more information")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-lease'] == 'cancel':
        sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
        transaction = CancelLease(lease_id=name_space.leaseId[0])
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease cancel --help' for more information")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-lease'] == 'out':
        node = handle.get_node(chain_id, parser)
        address = handle.get_account(chain_id, parser, account_name).address
        value = node.lease_list(address)
        flag = 0
        for x in value:
            if x['sender'] == address:  # outbound
                print(x['recipient'], ':', x['amount'] /100000000)
                flag +=1
        if flag == 0:
            print("No outbound leases")

    elif vars(name_space)['subparser-name-lease'] == 'in':
        node = handle.get_node(chain_id, parser)
        address = handle.get_account(chain_id, parser, account_name).address
        value = node.lease_list(address)
        flag = 0
        for x in value:
            if x['recipient'] == address:  # inbound
                print(x['sender'], ':', x['amount'] / 100000000)
                flag +=1
        if flag == 0:
            print("No inbound leases")

    else:
        parser.error("Unknown command. Type 'lto lease --help' for more information.")
