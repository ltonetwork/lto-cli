import argparse
import sys

from lto_cli import config
from lto_cli.commands import transfer
from lto_cli.commands import burn
from lto_cli.commands import anchor
from lto_cli.commands import leasing
from lto_cli.commands import sponsorship
from lto_cli.commands import association
from lto_cli.commands import account
from lto_cli.commands import mass_transfer
from lto_cli.commands import broadcast
from lto_cli.commands import balance
from lto_cli.commands import node
from lto_cli.commands import data
from importlib_metadata import version

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

    parser.add_argument('--version', action='store_true', required=False, help="Display the version of the package")
    subparsers = parser.add_subparsers(dest='subparser-name', help='sub-command help')

    # --------------------------------------------------------------
    parser_data = subparsers.add_parser('data', help="Create a data transaction or get the data associated with one account, type 'lto data --help' for more informations")
    data_subparser = parser_data.add_subparsers(dest='subparser-name-data')

    parser_set = data_subparser.add_parser('set', help="Create a data transaction, for more information on how to pipe the data type 'lto data set --help")
    parser_set.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,  help="Takes the data as input: echo 'my data' | lto data set")
    parser_set.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_set.add_argument('--network', type=str, nargs=1, required=False, help='Optional network parameter, if not specified default is L')
    parser_set.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    parser_set.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_set.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")

    parser_get = data_subparser.add_parser('get', help="Retrive the data associated with one account, if not specified the default account is selected, for more infotmations type 'lto data get --help")
    parser_get.add_argument('address', nargs='?', type=str, help='Insert the desired account address')
    parser_get.add_argument('--key', type=str, nargs=1, required=False, help="Use this option to retrieve the value of a specific entry")
    parser_get.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_get.add_argument('--network', type=str, nargs=1, required=False, help='Optional network parameter, if not specified default is L')

    # --------------------------------------------------------------
    parser_account = subparsers.add_parser('account', help="Create remove and manage accounts, type 'lto account --help' for more informations")
    account_subparser = parser_account.add_subparsers(dest='subparser-name-account')

    parser_create = account_subparser.add_parser('create', help="Allow to create an account with two optional parameter, --name and --network")
    parser_create.add_argument('--name', required=False, type=str, nargs=1)
    parser_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')

    parser_list = account_subparser.add_parser('list', help="Returns the list of accounts stored locally")
    parser_list.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_setDefault = account_subparser.add_parser('set-default', help="Sets the specified account as default account")
    parser_setDefault.add_argument('address', type=str, nargs=1)
    parser_setDefault.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_remove = account_subparser.add_parser('remove', help="Remove an account, if not specified, the default account is selected")
    parser_remove.add_argument('address', nargs='?', type=str, help='Insert the desired account address')
    parser_remove.add_argument('--account', type=str, nargs=1, required=False, help="Remove the specified account, the account can be identified by address or name")
    parser_remove.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')


    parser_show = account_subparser.add_parser('show', help="Show the information about the account, if not specified, the default account is selected")
    parser_show.add_argument('address', nargs='?', type=str, help='Insert the desired account address')
    parser_show.add_argument('--account', type=str, nargs=1, required=False, help="The account can be identified by address or name")
    parser_show.add_argument('--network', type=str, nargs=1, required=False, help='Optional network parameter, if not specified default is L')


    parser_seed = account_subparser.add_parser('seed', help="Create an account from seed, for more information on how to pipe the seed type 'lto account seed --help")
    parser_seed.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Takes the seeds as input: echo 'my seed' | lto account seed")
    parser_seed.add_argument('--name', required=False, type=str, nargs=1)
    parser_seed.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    # --------------------------------------------------------------
    parser_balance = subparsers.add_parser('balance', help="Get the account balance, if not specified the default account is selected")
    parser_balance.add_argument('address', nargs='?', type=str, help='Insert the desired account address')
    parser_balance.add_argument('--account', type=str, nargs=1, required=False, help="The account can be identified by address or name. In addition, an address of an account not stored locally can also be used")
    parser_balance.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_balance.add_argument('--regular', action='store_true', required=False, help="Use this option to show the regular balance")
    parser_balance.add_argument('--generating', action='store_true', required=False, help="Use this option to show the generating balance")
    parser_balance.add_argument('--available', action='store_true', required=False, help="Use this option to show the available balance")
    parser_balance.add_argument('--effective', action='store_true', required=False, help="Use this option to to show the effective balance")

    # --------------------------------------------------------------
    parser_anchor = subparsers.add_parser(name='anchor', help="Create an Anchor Transaction, type 'lto anchor --help' for more information")
    parser_anchor.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,  help="Takes the hash as input: echo 'my hahs' | lto anchor")
    parser_anchor.add_argument('--hash', type=str, nargs=1, help="The hash that will be anchored to the chain")
    parser_anchor.add_argument('--algo', type=str , nargs=1, required=False, help="Use this option to specify an algorithm to hash the input file")
    parser_anchor.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_anchor.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_anchor.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_anchor.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_anchor.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    parser_anchor.add_argument('--encoding', type=str , nargs=1, required=False, help="Use this option to provide the hash in a different encoding then hexadecimal (base58 or base64)")
    # --------------------------------------------------------------
    parser_association = subparsers.add_parser('association', help="Create an Association Transaction, type 'lto association --help' for more information")
    association_subparser = parser_association.add_subparsers(dest='subparser-name-association')

    parser_association_incoming = association_subparser.add_parser('incoming', help="Show the incomgin associations related to an account")
    parser_association_incoming.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_association_incoming.add_argument('--network', type=str, nargs=1, required=False, help='Optional network parameter, if not specified default is L')

    parser_association_outgoing = association_subparser.add_parser('outgoing', help="Show the incomgin associations related to an account")
    parser_association_outgoing.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_association_outgoing.add_argument('--network', type=str, nargs=1, required=False, help='Optional network parameter, if not specified default is L')

    parser_association_issue = association_subparser.add_parser('issue', help="Create an association transaction")
    parser_association_issue.add_argument('--hash', type=str, nargs=1, help = "Optional hash argument")
    parser_association_issue.add_argument('--recipient', type=str, nargs=1, required=True, help= 'The recipient')
    parser_association_issue.add_argument('--type', type=int, nargs=1, required=True, help='The association type')
    parser_association_issue.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_association_issue.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_association_issue.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_association_issue.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_association_issue.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")


    parser_association_revoke = association_subparser.add_parser('revoke', help="Create a revoke association transaction")
    parser_association_revoke.add_argument('--hash', type=str, nargs=1, help = "Optional hash argument")
    parser_association_revoke.add_argument('--recipient', type=str, nargs=1, required=True, help= 'The recipient')
    parser_association_revoke.add_argument('--type', type=int, nargs=1, required=True, help='The association type')
    parser_association_revoke.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_association_revoke.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_association_revoke.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_association_revoke.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_association_revoke.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
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

    parser_lease_create = lease_subparser.add_parser('create', help='To create a lease, --recipient and --amount are required')
    parser_lease_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_lease_create.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_lease_create.add_argument('--amount', type=float, nargs=1, required=True)
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

    parser_lease_incoming = lease_subparser.add_parser('incoming', help="Returns the list of leasing that the user has conceded")
    parser_lease_incoming.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_incoming.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')

    parser_lease_list_outgoing = lease_subparser.add_parser('outgoing', help="Returns the list of leasing in favor of the user")
    parser_lease_list_outgoing.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_lease_list_outgoing.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
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
    parser_node = subparsers.add_parser('node', help="Allows to performs operation regarding the node, type 'lto node --help' for more information")
    node_subparser = parser_node.add_subparsers(dest='subparser-name-node')

    parser_node_set = node_subparser.add_parser('set', help="Allows to set the preferred node to connect to and an optional network parameter, type 'lto node set --help' for more information")
    parser_node_set.add_argument('url', type=str, nargs=1, help="url of the node to connect to")
    parser_node_set.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')

    parser_node_show = node_subparser.add_parser('show', help="Displays the node url, type 'lto node show --help' for more information")
    parser_node_show.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')

    parser_node_status = node_subparser.add_parser('status', help="Allows to show the status of the node, type 'lto node status --help' for more information")
    parser_node_status.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')





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

    parser_sponsorship_outgoing = sponsorship_subparser.add_parser('outgoing', help="Returns the list of accounts that are sponsoring the user")
    parser_sponsorship_outgoing.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_sponsorship_outgoing.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    # --------------------------------------------------------------
    parser_transfer = subparsers.add_parser('transfer', help="Create a Transfer Transaction, type 'lto transfer --help' for more information")
    parser_transfer.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_transfer.add_argument('--amount', type=float, nargs=1, required=True)
    parser_transfer.add_argument('--account', type=str , nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_transfer.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter, if not specified default is L')
    parser_transfer.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_transfer.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_transfer.add_argument('--sponsor', type=str , nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")
    # --------------------------------------------------------------
    parser_burn = subparsers.add_parser('burn', help="Create a Burn Transaction, type 'lto burn --help' for more informations")
    parser_burn.add_argument('--amount', type=float, nargs=1, required=True, help="Specify the amounts of token to burn, 1 equals 1 LTO")
    parser_burn.add_argument('--account', type=str, nargs=1, required=False, help="Use this option to select one of the accounts previously stored. The account can be referenced by name or address, if this option is omitted, the default account is used")
    parser_burn.add_argument('--network', type=str, nargs=1, required=False,  help='Optional network parameter, if not specified default is L')
    parser_burn.add_argument('--no-broadcast', action='store_true', required=False, help="Use this option to not broadcast the transaction to the node")
    parser_burn.add_argument('--unsigned', action='store_true', required=False, help="Use this option to not sign the transaction. Use in combination with the '--no-broadcast' option")
    parser_burn.add_argument('--sponsor', type=str, nargs=1, required=False, help="Use this option to select an account for sponsoring the transaction")

    process_args(parser.parse_args(), parser)

def process_args(name_space, parser):

    if vars(name_space)['version']:
        print('Version:', version('lto_cli'))

    elif vars(name_space)['subparser-name'] == 'account':
        account.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'anchor':
        anchor.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'transfer':
        transfer.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'burn':
        burn.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'sponsorship':
        sponsorship.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'association':
        association.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'mass-transfer':
        mass_transfer.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'lease':
        leasing.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'node':
        node.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'broadcast':
        broadcast.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'balance':
        balance.func(name_space, parser)

    elif vars(name_space)['subparser-name'] == 'data':
        data.func(name_space, parser)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()