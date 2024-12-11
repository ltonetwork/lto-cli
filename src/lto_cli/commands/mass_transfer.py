from lto.transactions.mass_transfer import MassTransfer
from lto_cli import handle_default as handle
import sys
import re


def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    if unsigned and not no_broadcast:
        parser.error(
            "Use '--unsigned' only in combination with '--no-broadcast'. Type 'lto mass-transfer --help' for more information")

    stdin = name_space.stdin.read().splitlines()
    if not stdin:
        parser.error('Type lto mass-transfer --help for instructions')
    transfers = process_input(stdin)
    transaction = MassTransfer(transfers)

    transaction = handle.sign_and_broadcast(chain_id, parser, transaction, unsigned, no_broadcast, account_name,
                                            sponsor)
    handle.pretty_print(transaction)


def process_input(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = re.split(r'[,;:=\s]+', x)
        transfers.append({'recipient': recipient, 'amount': int(float(amount) * 100000000)})
    return transfers
