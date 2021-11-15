from LTOCli import handle_default as handle
from LTO.Transactions.transfer import Transfer

def func(name_space, parser):

    recipient = name_space.recipient[0]
    amount = name_space.amount[0]
    transaction = Transfer(recipient, amount)

    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''

    if vars(name_space)['unsigned'] is False:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
    elif vars(name_space)['no_broadcast'] is False:
        parser.error("Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto transaction --help' for more informations ")
    handle.pretty_print(transaction)