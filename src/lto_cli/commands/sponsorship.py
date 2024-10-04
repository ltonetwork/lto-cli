from lto_cli import handle_default as handle
from lto.transactions.sponsorship import Sponsorship
from lto.transactions.cancel_sponsorship import CancelSponsorship


def func(name_space, parser, subparser):
    if not vars(name_space)['subparser-name-sponsorship']:
        subparser.print_help()
        return
        
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

    if vars(name_space)['subparser-name-sponsorship'] == 'create':
        recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
        transaction = Sponsorship(recipient)
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship create --help' for more information")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-sponsorship'] == 'cancel':
        recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
        transaction = CancelSponsorship(recipient)
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship cancel --help' for more information")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-sponsorship'] == 'out':
        parser.error("Listing outbound sponsorships is not supported")

    else:  # inbound
        node = handle.get_node(chain_id, parser)
        address = handle.get_account(chain_id, parser, account_name).address
        value = node.sponsorship_list(address)
        if value['sponsor']:
            for x in value['sponsor']:
                print(x)
        else:
            print('Not sponsered')

