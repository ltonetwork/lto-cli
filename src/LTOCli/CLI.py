import argparse
import sys
from pathlib import Path
import os

from LTOCli import Config
from LTOCli.Commands import Transfer
from LTOCli.Commands import Anchor
from LTOCli.Commands import Leasing
from LTOCli.Commands import Sponsorhip, Association, Account
from LTOCli.Commands import MassTransfer

# IF ERROR MODULE NOT FOUND:
# export PYTHONPATH=$PYTHONPATH:'pwd.../lto-api.python'

def main():
    Config.checkDirectory()

    parser = argparse.ArgumentParser(prog='lto', description='LTO Network CLI client, visit the github page for more information https://github.com/ltonetwork/lto-cli',  usage=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest='subparser-name', help='sub-command help')

    # --------------------------------------------------------------
    parser_accounts = subparsers.add_parser('accounts', help="Create remove and manage accounts, type 'lto accounts --help' for more informations")
    accounts_subparser = parser_accounts.add_subparsers(dest='subparser-name-accounts')

    parser_create = accounts_subparser.add_parser('create', help="Allow to create an account with two optional parameter, --name and --network")
    parser_create.add_argument('--name', required=False, type=str, nargs=1)
    parser_create.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter (ex. L, T)')

    parser_list = accounts_subparser.add_parser('list', help="Returns the list of accounts stored locally")

    parser_setDefault = accounts_subparser.add_parser('set-default', help="Sets the specified account as default account")
    parser_setDefault.add_argument('address', type=str, nargs=1)

    parser_remove = accounts_subparser.add_parser('remove', help="Remove the specified account, the account can be identified by address or name")
    parser_remove.add_argument('address', type=str, nargs=1)

    parser_seed = accounts_subparser.add_parser('seed', help="Create an account from seed, for more information on how to pipe the seed type 'lto accounts seed --help")
    parser_seed.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                             help="Takes the seeds as input: echo 'my seed' | lto accounts seed")
    parser_seed.add_argument('--name', required=False, type=str, nargs=1)
    parser_seed.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter (ex. L, T)')
    # --------------------------------------------------------------
    parser_anchor = subparsers.add_parser(name='anchor', help="Create an Anchor Transaction, type 'lto anchor --help' for more information")
    parser_anchor.add_argument('--hash', type=str, nargs=1, help="The hash that will be anchored to the chain")
    # --------------------------------------------------------------
    parser_association = subparsers.add_parser('association', help="Create an Association Transaction, type 'lto association --help' for more information")
    parser_association.add_argument('option', type=str, choices=['issue', 'revoke'], nargs=1, help='issue / revoke')
    parser_association.add_argument('--hash', type=str, nargs=1, help = "Optional hash argument")
    parser_association.add_argument('--recipient', type=str, nargs=1, required=True, help= 'The recipient')
    parser_association.add_argument('--type', type=int, nargs=1, required=True, help='The association type')
    # --------------------------------------------------------------
    parser_lease = subparsers.add_parser('lease', help="Create a Lease Transaction, type 'lto lease --help' for more information")
    lease_subparser = parser_lease.add_subparsers(dest='subparser-name-lease')

    parser_lease_create = lease_subparser.add_parser('create', help='To create a lease, --recipient and --amount are requirede')
    parser_lease_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_lease_create.add_argument('--amount', type=int, nargs=1, required=True)

    parser_lease_cancel = lease_subparser.add_parser('cancel', help="To cancel a lease --leaseId is required")
    parser_lease_cancel.add_argument('--leaseId', type=str, nargs=1, required=True)
    # --------------------------------------------------------------
    parser_massTransfer = subparsers.add_parser('mass-transfer', help="Create an Mass-Transfer Transaction, type 'lto mass-transfer --help' for more information")
    parser_massTransfer.add_argument('stdin', nargs='?', type=argparse.FileType('r'),
                                     default=sys.stdin, help="Takes the transfers as input: echo 'address1:amount address2:amount' | lto mass-transfer")
    # --------------------------------------------------------------
    parser_setNode = subparsers.add_parser('set-node', help="Allows to set the preferred node to connect to and an optional network parameter, type 'lto set-node --help' for more information")
    parser_setNode.add_argument('url', type=str, nargs=1, help="url of the node to connect to")
    parser_setNode.add_argument('--network', type=str, nargs=1, required=False, help ='Optional network parameter (ex. L, T)')
    # --------------------------------------------------------------
    parser_sponsorship = subparsers.add_parser('sponsorship', help="Create an Sponsorship Transaction, type 'lto sponsorship --help' for more information")
    parser_sponsorship.add_argument('option', choices=['create', 'cancel'], help='create / cancel', type=str, nargs=1)
    parser_sponsorship.add_argument('--recipient', type=str, nargs=1)
    # --------------------------------------------------------------
    parser_transfer = subparsers.add_parser('transfer', help="Create a Transfer Transaction, type 'lto transfer --help' for more information")
    parser_transfer.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_transfer.add_argument('--amount', type=int, nargs=1, required=True)






    nameSpace = parser.parse_args()
    #nameSpace = parser.parse_args(['accounts','seed','--help'])
    #nameSpace = parser.parse_args()
    processArgs(nameSpace, parser)

def processArgs(nameSpace, parser):

    if vars(nameSpace)['subparser-name'] == 'accounts':
        Account.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'anchor':
        Anchor.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'transfer':
        Transfer.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'sponsorship':
        Sponsorhip.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'association':
        Association.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'mass-transfer':
        MassTransfer.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'lease':
        Leasing.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'set-node':
        Config.setnode(nameSpace)

    else:
        print("Type 'lto --help' for instructions")


if __name__ == '__main__':
    main()