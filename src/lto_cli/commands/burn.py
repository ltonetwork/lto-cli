from lto_cli import handle_default as handle
from lto.transactions.burn import Burn

def func(name_space, parser):

    amount = int(name_space.amount[0] * 100000000)
    transaction = Burn(amount)

    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None

    if vars(name_space)['unsigned'] is False:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if sponsor:
            transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
    elif vars(name_space)['no_broadcast'] is False:
        parser.error("Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto transaction --help' for more informations ")
    handle.pretty_print(transaction)