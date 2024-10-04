from lto.transactions.mass_transfer import MassTransfer
from lto_cli import handle_default as handle
import sys
import re

def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None

    stdin = name_space.stdin.read().splitlines()
    if not stdin:
        parser.error('Type lto mass-transfer --help for instructions')
    transfers = processInput(stdin)
    transaction = MassTransfer(transfers)
    if vars(name_space)['unsigned'] is False:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if sponsor:
            transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
    elif vars(name_space)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto mass-transfer --help' for more information")

    handle.pretty_print(transaction)

def processInput(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = re.split('[,;:=\s]+', x)
        transfers.append({'recipient': recipient, 'amount': int(float(amount) * 100000000)})
    return transfers
