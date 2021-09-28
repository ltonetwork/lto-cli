from LTO.AccountFactory import AccountFactory
from LTOCli import Config
import sys
import argparse

def func(nameSpace, parser):


    if vars(nameSpace)['subparser-name-accounts'] == 'create':
        CHAIN_ID = nameSpace.network[0] if nameSpace.network else 'L'
        secName = nameSpace.name[0] if nameSpace.name else ''
        factory = AccountFactory(CHAIN_ID)
        account = factory.create()
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)

    elif vars(nameSpace)['subparser-name-accounts'] == 'list':
        listAcc = Config.listAccounts()
        for x in listAcc[0]:
            print(x)

    elif vars(nameSpace)['subparser-name-accounts'] == 'set-default':
        CHAIN_ID = nameSpace.network[0] if nameSpace.network else 'L'
        Config.setDefaultAccount(nameSpace.address[0], CHAIN_ID)

    elif vars(nameSpace)['subparser-name-accounts'] == 'remove':
        Config.removeAccount(nameSpace.address[0], parser)

    elif vars(nameSpace)['subparser-name-accounts'] == 'seed':
        CHAIN_ID = nameSpace.network[0] if nameSpace.network else 'L'
        secName = nameSpace.name[0] if nameSpace.name else ''
        factory = AccountFactory(CHAIN_ID)
        seed = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
        if not seed:
            parser.error('Type lto accounts seed --help for instructions') # add the correct message here
        account = factory.createFromSeed(seed[0])
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName, parser)
    else:
        parser.error('Type lto accounts --help for instructions')
