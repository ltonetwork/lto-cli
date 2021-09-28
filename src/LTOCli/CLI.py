import argparse
import sys

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
    if not os.path.exists('L'):
        os.mkdir(path='./L')
    if not os.path.exists('T'):
        os.mkdir(path='./T')


    '''parser = argparse.ArgumentParser(description='LTO Network CLI client', usage=argparse.SUPPRESS)
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=int, nargs=1)
    parser.add_argument('--leaseId', type=str, nargs=1)
    parser.add_argument('--network', type=str, nargs=1)
    parser.add_argument('--type', type=int, nargs=1)
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help=argparse.SUPPRESS)

    args = parser.parse_args()
    processArgs(args, parser)'''

    parser = argparse.ArgumentParser(prog='lto', description='LTO Network CLI client')  # , usage=argparse.SUPPRESS)
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

    parser_transfer = subparsers.add_parser('transfer', help='b help')
    parser_transfer.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_transfer.add_argument('--amount', type=int, nargs=1, required=True)

    parser_sponsorship = subparsers.add_parser('sponsorship', help='b help')
    parser_sponsorship.add_argument('option', choices=['create', 'cancel'], help='create / cancel', type=str, nargs=1)
    parser_sponsorship.add_argument('--recipient', type=str, nargs=1)

    parser_massTransfer = subparsers.add_parser('mass-transfer')
    parser_massTransfer.add_argument('stdin', nargs='?', type=argparse.FileType('r'),
                                     default=sys.stdin, help="Takes the transfers as input: echo 'address1:amount address2:amount' | lto mass-transfer")#, help=argparse.SUPPRESS)

    # --------------------------------------------------------------
    parser_lease = subparsers.add_parser('lease', help='b help')
    lease_subparser = parser_lease.add_subparsers(dest='subparser-name-lease')

    parser_lease_create = lease_subparser.add_parser('create')
    parser_lease_create.add_argument('--recipient', type=str, nargs=1, required=True)
    parser_lease_create.add_argument('--amount', type=int, nargs=1, required=True)

    parser_lease_cancel = lease_subparser.add_parser('cancel')
    parser_lease_cancel.add_argument('--leaseId', type=str, nargs=1, required=True)

    # --------------------------------------------------------------
    parser_accounts = subparsers.add_parser('accounts', help='b help')
    accounts_subparser = parser_accounts.add_subparsers(dest='subparser-name-accounts')

    parser_create = accounts_subparser.add_parser('create')
    parser_list = accounts_subparser.add_parser('list')

    parser_setDefault = accounts_subparser.add_parser('set-default')
    parser_setDefault.add_argument('address', type=str, nargs=1)

    parser_remove = accounts_subparser.add_parser('remove')
    parser_remove.add_argument('address', type=str, nargs=1)

    parser_seed = accounts_subparser.add_parser('seed')
    parser_seed.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    nameSpace = parser.parse_args(['lease', 'cancel', '--leaseId', 'kjhkh'])
    #nameSpace = parser.parse_args(['accounts'])
    #nameSpace = parser.parse_args()
    processArgs(nameSpace, parser)

def processArgs(nameSpace, parser):
    '''args         = arguments.list
    name         = arguments.name
    hash         = arguments.hash
    recipient    = arguments.recipient
    amount       = arguments.amount
    leaseId      = arguments.leaseId
    network      = arguments.network
    type         = arguments.type
    stdin        = arguments.stdin.read().splitlines() if not sys.stdin.isatty() else []

    if name:
        name = name[0]'''

    if vars(nameSpace)['subparser-name'] == 'accounts':
        Account.func(nameSpace, parser)
    elif vars(nameSpace)['subparser-name'] == 'anchor':
        Anchor.func(nameSpace)
    elif vars(nameSpace)['subparser-name'] == 'transfer':
        Transfer.func(nameSpace)

    elif vars(nameSpace)['subparser-name'] == 'sponsorship':
        Sponsorhip.func(nameSpace)

    elif vars(nameSpace)['subparser-name'] == 'association':
        Association.func(nameSpace)

    elif vars(nameSpace)['subparser-name'] == 'mass-transfer':
        MassTransfer.func(nameSpace, parser)

    elif vars(nameSpace)['subparser-name'] == 'lease':
        Leasing.func(nameSpace, parser)

    '''elif args[0] == 'association':
        Association.func(args, type, recipient, hash)
    elif args[0] == 'lease':
        Leasing.func(args, recipient, amount, leaseId)
    elif args[0] == 'sponsorship':
        Sponsorhip.func(args, recipient)
    elif args[0] == 'set-node':
        Config.setnode(args, network)
    elif args[0] == 'mass-transfer':
        MassTransfer.func(stdin)
    else:
        parser.error('Unrecognized input')'''


if __name__ == '__main__':
    main()