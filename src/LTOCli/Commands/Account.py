from LTO.AccountFactory import AccountFactory
from LTOCli import Config
import argparse

def func(args, secName, network, stdin):

    parser2 = argparse.ArgumentParser(description='second parser')
    parser2.add_argument('lto', type=str, nargs='+')
    args2 = parser2.parse_args()
    print(args2)
    if not network:
        CHAIN_ID = 'L'
    else:
        CHAIN_ID = network[0]

    factory = AccountFactory(CHAIN_ID)
    if len(args) > 1:
        if args[1] == 'create':
            account = factory.create()
            Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)
        elif args[1] == 'list':
            listAcc = Config.listAccounts()
            for x in listAcc[0]:
                print(x)
        elif args[1] == 'remove':
            Config.removeAccount(args[2])
        elif args[1] == 'set-default':
            Config.setDefaultAccount(args[2])
        elif args[1] == 'seed':
            account = factory.createFromSeed(stdin[0])
            Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)
        else:
            parser2.error('Unrecognized input')
    else:
        parser2.error('Type lto accounts --help for instructions')
