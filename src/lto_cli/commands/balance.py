from lto_cli import handle_default as handle


def print_balance(name_space, balances):
    types = vars(name_space)['types']

    if types is None or 'regular' in types:
        print('Regular:   ', balances['regular'] / 100000000)
    if types is None or 'available' in types:
        print('Available: ', balances['available'] / 100000000)
    if types is None or 'leasing' in types:
        print('Leasing:   ', balances['leasing'] / 100000000)
    if types is None or 'unbonding' in types:
        print('Unbonding: ', balances['unbonding'] / 100000000)
    if types is None or 'effective' in types:
        print('Effective: ', balances['effective'] / 100000000)
    if types is None or 'generating' in types:
        print('Generating:', balances['generating'] / 100000000)


def validate_address(address, node):
    return node.validate_address(address)


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    address = name_space.address if name_space.address else None
    if not address:
        address = name_space.account[0] if name_space.account else handle.get_account(chain_id, parser).address
    node = handle.get_node(chain_id, parser)

    if validate_address(address, node):
        balances = node.balance_details(address)
        print_balance(name_space, balances)
    else:
        account = handle.get_account(chain_id, parser, address)
        balances = node.balance_details(account.address)
        print_balance(name_space, balances)

