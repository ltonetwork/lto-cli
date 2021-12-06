from lto_cli import handle_default as handle


def print_balance(name_space, balances):
    if vars(name_space)['regular'] is False and \
            vars(name_space)['available'] is False and \
            vars(name_space)['generating'] is False and \
            vars(name_space)['effective'] is False:
        print('Regular: ', balances['regular'] / 100000000,
              '\nGenerating: ', balances['generating'] / 100000000,
              '\nAvailable: ', balances['available'] / 100000000,
              '\nEffective: ', balances['effective']/ 100000000,)
    else:
        if vars(name_space)['regular'] is True:
            print('Regular: ', balances['regular'] / 100000000)
        if vars(name_space)['generating'] is True:
            print('Generating: ', balances['generating'] / 100000000)
        if vars(name_space)['available'] is True:
            print('Available: ', balances['available'] / 100000000)
        if vars(name_space)['effective'] is True:
            print('Effective: ', balances['effective'] / 100000000)


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    id = name_space.id[0] if name_space.id else handle.get_account(chain_id, parser).address

    #account_name = vars(name_space)['account'] if vars(name_space)['account'] else ''

    node = handle.get_node(chain_id, parser)
    try:
        account = handle.get_account_for_balance(chain_id, parser, id)
        balances = node.balance_details(account.address)
        print_balance(name_space, balances)
    except:
        try:
            balances = node.balance_details(id)
            print_balance(name_space, balances)
        except:
            parser.error("Address not valid, type 'lto account --help' for instructions")

