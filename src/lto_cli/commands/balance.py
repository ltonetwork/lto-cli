from lto_cli import handle_default as handle


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'] if vars(name_space)['account'] else ''

    node = handle.get_node(chain_id, parser)
    account = handle.get_account(chain_id, parser, account_name)

    balances = node.balance_details(account.address)

    if vars(name_space)['regular'] is False and \
            vars(name_space)['available'] is False and \
            vars(name_space)['generating'] is False and \
            vars(name_space)['effective'] is False:
        print('Regular: ', balances['regular'],
              '\nGenerating: ', balances['generating'],
              '\nAvailable: ', balances['available'],
              '\nEffective: ', balances['effective'],)
    else:
        if vars(name_space)['regular'] is True:
            print('Regular: ', balances['regular'])
        if vars(name_space)['generating'] is True:
            print('Generating: ', balances['generating'])
        if vars(name_space)['available'] is True:
            print('Available: ', balances['available'])
        if vars(name_space)['effective'] is True:
            print('Effective: ', balances['effective'])






#  * 3JwNzwwSa4x9KxYv8k8Sb8ZXKxDg5q7ZnJk

# * 3MvtN3EpTzzzMwD6SQNrUjtJGpx4tnrZCmo  -  found
#   3N34SdbTa5aRpVQmC9ZoQ3ruAp67ZvH2sU6  -  test
#   3Mwy4ntCyVDbfPegA1gJmXKJSz79wkBuC6G