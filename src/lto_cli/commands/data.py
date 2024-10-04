import json

from lto_cli import handle_default as handle
from lto.transactions.data import Data

from lto_cli.handle_default import validate_address


def data_set(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    data = name_space.stdin.read()
    if not data:
        parser.error("Data missing, type 'lto data set --help' for instructions")

    transaction = Data(json.loads(data))
    if vars(name_space)['unsigned'] is False:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if sponsor:
            transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
    elif vars(name_space)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor "
            "--help' for more information")
    handle.pretty_print(transaction)


def data_get(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    key = name_space.key[0] if name_space.key else None
    address = name_space.address if name_space.address else None
    if not address:
        address = handle.get_account(chain_id, parser).address
    node = handle.get_node(chain_id, parser)
    if not validate_address(address):
        parser.error(f'{address} address is not valid')
    if key:
        value = node.get_data_by_key(address, key)
        if not value:
            print(f'No data found for {address}')
        else:
            print(value)
    else:
        value = node.get_data(address)
        if not value:
            print(f'No data found for {address}')
        else:
            for x in value:
                print(x)


def func(name_space, parser, subparser):
    if vars(name_space)['subparser-name-data'] == 'set':
        data_set(name_space, parser)

    elif vars(name_space)['subparser-name-data'] == 'get':
        data_get(name_space, parser)

    else:
        subparser.print_help()

