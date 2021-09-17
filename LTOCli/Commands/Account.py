from LTO.AccountFactory import AccountFactory
from LTOCli import Config


def func(args, secName, network, stdin):
    if not network:
        CHAIN_ID = 'L'
    else:
        CHAIN_ID = network[0]

    factory = AccountFactory(CHAIN_ID)

    if args[1] == 'create':
        account = factory.create()
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)
    elif args[1] == 'list':
        print(Config.listAccounts())
    elif args[1] == 'remove':
        Config.removeAccount(args[2])
    elif args[1] == 'set-default':
        Config.setDefaultAccount(args[2])
    elif args[1] == 'seed':
        account = factory.createFromSeed(stdin[0])
        Config.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)
