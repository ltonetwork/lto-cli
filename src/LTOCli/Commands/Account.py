from LTO.AccountFactory import AccountFactory
from LTOCli import Config
import sys
import argparse

def func(nameSpace, parser):
    CHAIN_ID = 'L' # set if specified, can be specified under network
    secName = '' # if not secName, the name can be specified as an option
    factory = AccountFactory(CHAIN_ID)

    if vars(nameSpace)['subparser-name-accounts'] == 'create':
        account = factory.create()
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)

    if vars(nameSpace)['subparser-name-accounts'] == 'list':
        listAcc = Config.listAccounts()
        for x in listAcc[0]:
            print(x)

    if vars(nameSpace)['subparser-name-accounts'] == 'set-default':
        Config.setDefaultAccount(nameSpace.address[0])

    if vars(nameSpace)['subparser-name-accounts'] == 'remove':
        Config.removeAccount(nameSpace.address[0])

    if vars(nameSpace)['subparser-name-accounts'] == 'seed':
        seed = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
        if not seed:
            parser.error('Type lto accounts --help for instructions') # add the correct message here
        account = factory.createFromSeed(seed[0])
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)

