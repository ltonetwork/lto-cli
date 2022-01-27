import json
from lto.transactions import from_data
from lto_cli import handle_default as handle


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    node = handle.get_node(chain_id, parser)
    tx_json = name_space.stdin.read()
    if not tx_json:
        parser.error("Expected transaction as input, type 'lto broadcast --help' for instructions")

    transaction = from_data(json.loads(tx_json))

    if vars(name_space)['unsigned'] is False:
        if not transaction.proofs:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(node)
    else:
        if not transaction.proofs:
            parser.error("Transaction needs to be signed before broadcasting, type 'lto broadcast --help' for instruction")
        else:
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(node)

    handle.pretty_print(transaction)


