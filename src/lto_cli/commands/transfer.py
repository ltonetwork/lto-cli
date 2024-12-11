from lto_cli import handle_default as handle
from lto.transactions.transfer import Transfer

def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    recipient = handle.get_address(chain_id, parser, name_space.recipient[0])
    amount = int(name_space.amount[0] * 100000000)

    if unsigned and not no_broadcast:
        parser.error("Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto transfer --help' for more information")

    transaction = Transfer(recipient, amount)

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
    handle.pretty_print(transaction)
