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

    parser = argparse.ArgumentParser(prog='lto', description='LTO Network CLI client',  usage=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest='subparser-name', help='sub-command help')

    parser_anchor = subparsers.add_parser(name='anchor', help='a help')
    parser_anchor.add_argument('--hash', type=str, nargs=1)

    parser_association = subparsers.add_parser('association', help='b help')
    parser_association.add_argument('option', type=str, choices=['issue', 'revoke'], nargs=1, help='issue / revoke')
    parser_association.add_argument('--hash', type=str, nargs=1)
    parser_association.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_association.add_argument('--type', type=int, nargs=1, required=True)

    parser_setNode = subparsers.add_parser('set-node', help='b help')
    parser_setNode.add_argument('url', type=str, nargs=1)
    parser_setNode.add_argument('--network', type=str, nargs=1, required=False)

    parser_transfer = subparsers.add_parser('transfer', help='b help')
    parser_transfer.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_transfer.add_argument('--amount', type=int, nargs=1, required=True)

    parser_sponsorship = subparsers.add_parser('sponsorship', help='b help')
    parser_sponsorship.add_argument('option', choices=['create', 'cancel'], help='create / cancel', type=str, nargs=1)
    parser_sponsorship.add_argument('--recipient', type=str, nargs=1)

    parser_massTransfer = subparsers.add_parser('mass-transfer')
    parser_massTransfer.add_argument('stdin', nargs='?', type=argparse.FileType('r'),
                                     default=sys.stdin, help="Takes the transfers as input: echo 'address1:amount address2:amount' | lto mass-transfer")

    # --------------------------------------------------------------
    parser_lease = subparsers.add_parser('lease', help='b help')
    lease_subparser = parser_lease.add_subparsers(dest='subparser-name-lease')

    parser_lease_create = lease_subparser.add_parser('create')
    parser_lease_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_lease_create.add_argument('--amount', type=int, nargs=1, required=True)

    parser_lease_cancel = lease_subparser.add_parser('cancel')
    parser_lease_cancel.add_argument('--leaseId', type=str, nargs=1, required=True)

    # --------------------------------------------------------------
    parser_accounts = subparsers.add_parser('accounts')
    accounts_subparser = parser_accounts.add_subparsers(dest='subparser-name-accounts')

    parser_create = accounts_subparser.add_parser('create')
    parser_create.add_argument('--name', required=False, type=str, nargs=1)
    parser_create.add_argument('--network', type=str, nargs=1, required=False)


    parser_list = accounts_subparser.add_parser('list')

    parser_setDefault = accounts_subparser.add_parser('set-default')
    parser_setDefault.add_argument('address', type=str, nargs=1)

    parser_remove = accounts_subparser.add_parser('remove')
    parser_remove.add_argument('address', type=str, nargs=1)

    parser_seed = accounts_subparser.add_parser('seed')
    parser_seed.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                             help="Takes the seeds as input: echo 'my seed' | lto accounts seed")
    parser_seed.add_argument('--name', required=False, type=str, nargs=1)
    parser_seed.add_argument('--network', type=str, nargs=1, required=False)



    nameSpace = parser.parse_args(['accounts', 'create'])
    #nameSpace = parser.parse_args(['--help'])
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


if __name__ == '__main__':
    main()