import json

from lto_cli import handle_default as handle
from lto.transactions.data import Data

from lto_cli.handle_default import validate_address


def data_set(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    data = name_space.stdin.read()
    if not data:
        parser.error("Data missing, type 'lto data set --help' for instructions")

    transaction = Data(json.loads(data))

    if unsigned and not no_broadcast:
        parser.error(
            "Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto anchor "
            "--help' for more information")

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name, sponsor)
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
        value = node.data_by_key(address, key)
        if not value:
            print(f'No data found for {address}')
        else:
            print(value)
    else:
        value = node.data(address)
        if not value:
            print(f'No data found for {address}')
        else:
            print(json.dumps(value, indent=2))


def func(name_space, parser, subparser):
    if vars(name_space)['subparser-name-data'] == 'set':
        data_set(name_space, parser)

    elif vars(name_space)['subparser-name-data'] == 'get':
        data_get(name_space, parser)

    else:
        subparser.print_help()

