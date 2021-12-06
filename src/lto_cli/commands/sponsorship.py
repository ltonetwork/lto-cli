from lto_cli import handle_default as handle
from lto.transactions.sponsorship import Sponsorship
from lto.transactions.cancel_sponsorship import CancelSponsorship


def func(name_space,parser):
    if vars(name_space)['subparser-name-sponsorship']:
        chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
        account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

        if vars(name_space)['subparser-name-sponsorship'] == 'create':
            sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
            transaction = Sponsorship(name_space.recipient[0])
            if vars(name_space)['unsigned'] is False:
                transaction.sign_with(handle.get_account(chain_id, parser, account_name))
                if sponsor:
                    transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
                if vars(name_space)['no_broadcast'] is False:
                    transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
            elif vars(name_space)['no_broadcast'] is False:
                parser.error(
                    "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship create --help' for more informations ")
            handle.pretty_print(transaction)

        elif vars(name_space)['subparser-name-sponsorship'] == 'cancel':
            sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
            transaction = CancelSponsorship(name_space.recipient[0])
            if vars(name_space)['unsigned'] is False:
                transaction.sign_with(handle.get_account(chain_id, parser, account_name))
                if sponsor:
                    transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
                if vars(name_space)['no_broadcast'] is False:
                    transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
            elif vars(name_space)['no_broadcast'] is False:
                parser.error(
                    "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto sponsorship cancel --help' for more informations ")
            handle.pretty_print(transaction)

        elif vars(name_space)['subparser-name-sponsorship'] == 'list':
            pass

        else:  # outgoing
            node = handle.get_node(chain_id, parser)
            address = handle.get_account(chain_id, parser, account_name).address
            value = node.sponsorship_list(address)
            if value['sponsor']:
                for x in value['sponsor']:
                    print(x)
            else:
                print('No outgoing sponsorships found')

    else:
        parser.error('Type lto sponsorship --help for instructions')



