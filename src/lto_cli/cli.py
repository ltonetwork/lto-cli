import argparse
import sys

from lto_cli import config
from lto_cli.commands import transfer
from lto_cli.commands import anchor
from lto_cli.commands import leasing
from lto_cli.commands import sponsorship
from lto_cli.commands import association
from lto_cli.commands import account
from lto_cli.commands import mass_transfer
from lto_cli.commands import broadcast

# IF ERROR MODULE NOT FOUND:
# export PYTHONPATH=$PYTHONPATH:'pwd.../lto-api.python'

def main():
    config.check_directory()

    parser = argparse.ArgumentParser(prog='lto', description=''
'          _____       _____                    _______ \n'
'         /\    \     /\    \                  /::\    \ \n'
'        /::\____\   /::\    \                /::::\    \ \n'
'       /:::/    /   \:::\    \              /::::::\    \ \n'
'      /:::/    /     \:::\    \            /::::::::\    \ \n'
'     /:::/    /       \:::\    \          /:::/~~\:::\    \ \n'
'    /:::/    /         \:::\    \        /:::/    \:::\    \ \n'
'   /:::/    /          /::::\    \      /:::/    / \:::\    \ \n'
'  /:::/    /          /::::::\    \    /:::/____/   \:::\____\ \n'
' /:::/    /          /:::/\:::\    \  |:::|    |     |:::|    | \n'
'/:::/____/          /:::/  \:::\____\ |:::|____|     |:::|____| \n'
'\:::\    \         /:::/    \::/    /  \:::\    \   /:::/    / \n'
' \:::\    \       /:::/    / \/____/    \:::\    \ /:::/    / \n'
'  \:::\    \     /:::/    /              \:::\    /:::/    / \n'
'   \:::\    \   /:::/    /                \:::\__/:::/    / \n'
'    \:::\    \  \::/    /                  \::::::::/    / \n'
'     \:::\    \  \/____/                    \::::::/    / \n'
'      \:::\    \                             \::::/    / \n'
'       \:::\____\                             \::/____/ \n'
'        \::/    /                               \n'
'         \/____/ \n\n'
                                                             'LTO Network CLI client, visit the github page for more information https://github.com/ltonetwork/lto-cli',
                                     usage=argparse.SUPPRESS, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='subparser-name', help='sub-command help')

    # --------------------------------------------------------------
    parser_accounts = subparsers.add_parser('accounts', help="Create remove and manage accounts, type 'lto accounts --help' for more informations")
    accounts_subparser = parser_accounts.add_subparsers(dest='subparser-name-accounts')

    parser_create = accounts_subparser.add_parser('create', help="Allow to create an account with two optional parameter, --name and --network")
    parser_create.add_argument('--name', required=False, type=str, nargs=1)
    parser_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')

    parser_list = accounts_subparser.add_parser('list', help="Returns the list of accounts stored locally")
    parser_list.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_setDefault = accounts_subparser.add_parser('set-default', help="Sets the specified account as default account")
    parser_setDefault.add_argument('address', type=str, nargs=1)


    parser_remove = accounts_subparser.add_parser('remove', help="Remove the specified account, the account can be identified by address or name")
    parser_remove.add_argument('address', type=str, nargs=1)

    parser_show = accounts_subparser.add_parser('show', help="Show the information about the account")
    parser_show.add_argument('address', type=str, nargs=1, help="The address field can be filled with either address or name")

    parser_seed = accounts_subparser.add_parser('seed', help="Create an account from seed, for more information on how to pipe the seed type 'lto accounts seed --help")
    parser_seed.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Takes the seeds as input: echo 'my seed' | lto accounts seed")
    parser_seed.add_argument('--name', required=False, type=str, nargs=1)
    parser_seed.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    # --------------------------------------------------------------
    parser_anchor = subparsers.add_parser(name='anchor', help="Create an Anchor Transaction, type 'lto anchor --help' for more information")
    parser_anchor.add_argument('--hash', type=str, nargs=1, help="The hash that will be anchored to the chain", required=True)
    parser_anchor.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_anchor.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_anchor.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_anchor.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_anchor.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    # --------------------------------------------------------------
    parser_association = subparsers.add_parser('association', help="Create an Association Transaction, type 'lto association --help' for more information")
    parser_association.add_argument('option', type=str, choices=['issue', 'revoke'], nargs=1, help='issue / revoke')
    parser_association.add_argument('--hash', type=str, nargs=1, help = "Optional hash argument")
    parser_association.add_argument('--recipient', type=str, nargs=1, required=True, help= 'The recipient')
    parser_association.add_argument('--type', type=int, nargs=1, required=True, help='The association type')
    parser_association.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_association.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_association.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_association.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_association.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    # --------------------------------------------------------------
    parser_broadcast = subparsers.add_parser('broadcast', help="Takes as input a transaction (signed or unsigned) and broadcast it to the network, type 'lto broadcast --help' for more informations")
    parser_broadcast.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Takes the json transaction as input: echo '$TX_JSON' | lto broadcast")
    parser_broadcast.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored for signing the transaction. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_broadcast.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_broadcast.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_broadcast.add_argument('--unsigned', action='store_true', required=False, help="Use this option to ensure the transaction is already signed, and will not be signed by the CLI wallett")
    # --------------------------------------------------------------
    parser_lease = subparsers.add_parser('lease', help="Create a Lease Transaction, type 'lto lease --help' for more information")
    lease_subparser = parser_lease.add_subparsers(dest='subparser-name-lease')

    parser_lease_list = lease_subparser.add_parser('list', help="Returns the list of leasing that the user has conceded")
    parser_lease_list.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_list.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_lease_list_inbound = lease_subparser.add_parser('list-inbound', help="Returns the list of leasing in favor of the user")
    parser_lease_list_inbound.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_list_inbound.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_lease_create = lease_subparser.add_parser('create', help='To create a lease, --recipient and --amount are required')
    parser_lease_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_lease_create.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_lease_create.add_argument('--amount', type=int, nargs=1, required=True)
    parser_lease_create.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_lease_create.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_lease_create.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")

    parser_lease_cancel = lease_subparser.add_parser('cancel', help="To cancel a lease --leaseId is required")
    parser_lease_cancel.add_argument('--leaseId', type=str, nargs=1, required=True)
    parser_lease_cancel.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_cancel.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_lease_cancel.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_lease_cancel.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_lease_cancel.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    # --------------------------------------------------------------
    parser_massTransfer = subparsers.add_parser('mass-transfer', help="Create a Mass-Transfer Transaction, type 'lto mass-transfer --help' for more information")
    parser_massTransfer.add_argument('stdin', nargs='?', type=argparse.FileType('r'),
                                     default=sys.stdin, help="Takes the transfers as input: echo 'address1:amount address2:amount' | lto mass-transfer")
    parser_massTransfer.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_massTransfer.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_massTransfer.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_massTransfer.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_massTransfer.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    # --------------------------------------------------------------
    parser_setNode = subparsers.add_parser('set-node', help="Allows to set the preferred node to connect to and an optional network parameter, type 'lto set-node --help' for more information")
    parser_setNode.add_argument('url', type=str, nargs=1, help="url of the node to connect to")
    parser_setNode.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    # --------------------------------------------------------------
    parser_sponsorship = subparsers.add_parser('sponsorship', help="Create a Sponsorship Transaction, type 'lto sponsorship --help' for more information")
    sponsorship_subparser = parser_sponsorship.add_subparsers(dest='subparser-name-sponsorship')


    parser_sponsorship_create = sponsorship_subparser.add_parser('create',  help='To create a sponsorhip the --recipient is required')
    parser_sponsorship_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_sponsorship_create.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_sponsorship_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_sponsorship_create.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_sponsorship_create.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_sponsorship_create.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")


    parser_sponsorship_cancel = sponsorship_subparser.add_parser('cancel', help='To cancel a sponsorhip the --recipient is required')
    parser_sponsorship_cancel.add_argument('--recipient', type=str, nargs=1, required = True)
    parser_sponsorship_cancel.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_sponsorship_cancel.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_sponsorship_cancel.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_sponsorship_cancel.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_sponsorship_cancel.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")

    # The end-point needs to be added
    #parser_sponsorship_list = sponsorship_subparser.add_parser('list', help="Returns the list of accounts that the user is sponsoring")
    #parser_sponsorship_list.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")

    parser_sponsorship_list_inbound = sponsorship_subparser.add_parser('list-inbound', help="Returns the list of accounts that are sponsoring the user")
    parser_sponsorship_list_inbound.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_sponsorship_list_inbound.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    # --------------------------------------------------------------
    parser_transfer = subparsers.add_parser('transfer', help="Create a Transfer Transaction, type 'lto transfer --help' for more information")
    parser_transfer.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_transfer.add_argument('--amount', type=int, nargs=1, required=True)
    parser_transfer.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_transfer.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_transfer.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_transfer.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_transfer.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")

    process_args(parser.parse_args(), parser)

def process_args(name_space, parser):

    if vars(name_space)['subparser-name'] == 'accounts':
        account.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'anchor':
        anchor.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'transfer':
        transfer.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'sponsorship':
        sponsorship.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'association':
        association.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'mass-transfer':
        mass_transfer.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'lease':
        leasing.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'set-node':
        config.set_node(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'broadcast':
        broadcast.func(name_space, parser)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()