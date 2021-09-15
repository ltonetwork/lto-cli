import argparse
import sys
import Config
import os

from Commands import Account
from Commands import Transfer
from Commands import Anchor
from Commands import Association
from Commands import Leasing
from Commands import Sponsorhip
from Commands import MassTransfer

# IF ERROR MODULE NOT FOUND:
# export PYTHONPATH=$PYTHONPATH:'pwd.../lto-api.python'

def main():
    if not os.path.exists('L'):
        os.mkdir(path='./L')
    if not os.path.exists('T'):
        os.mkdir(path='./T')
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=int, nargs=1)
    parser.add_argument('--leaseId', type=str, nargs=1)
    parser.add_argument('--network', type=str, nargs=1)
    parser.add_argument('--type', type=int, nargs=1)
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args()
    processArgs(args, parser)





def processArgs(arguments, parser):
    args         = arguments.list
    name         = arguments.name
    hash         = arguments.hash
    recipient    = arguments.recipient
    amount       = arguments.amount
    leaseId      = arguments.leaseId
    network      = arguments.network
    type         = arguments.type
    stdin        = arguments.stdin.read().splitlines() if not sys.stdin.isatty() else []
    #stdin = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj:700000000', '3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz:1000000']
    #stdin2 = ['3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK:1000000000 3JxcLqcAKiUyvvLS8fk9SCS4taaCKUCqqLz:800000000']
    #stdinSeed = ['cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy']

    if name:
        name = name[0]

    if args[0] == 'accounts':
        Account.func(args, name, network, stdin)
    elif args[0] == 'anchor':
        Anchor.func(hash)
    elif args[0] == 'transfer':
        Transfer.func(recipient, amount)
    elif args[0] == 'association':
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
        parser.error('Unrecognized input')


if __name__ == '__main__':
    main()