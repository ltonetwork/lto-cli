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


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    node = handle.get_node(chain_id, parser)

    if name_space.address and name_space.account:
        parser.error('Specify an address or account, not both')

    if name_space.account:
        address = handle.get_account(chain_id, parser, name_space.account[0]).address
    elif name_space.address:
        address = handle.get_address(chain_id, parser, name_space.address)
    else:
        address = handle.get_account(chain_id, parser).address

    balances = node.balance_details(address)
    print_balance(name_space, balances)
