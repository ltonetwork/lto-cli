from LTO.Accounts.AccountFactoryED25519 import AccountED25519 as AccountFactory
from LTOCli import Config
import sys

def func(nameSpace, parser):
    if vars(nameSpace)['subparser-name-accounts'] == 'create':
        chainId = nameSpace.network[0] if nameSpace.network else 'L'
        if not (chainId.isalpha() and len(chainId) == 1):
            parser.error('The --network parameter accepts only CHAR type')
        chainId = chainId.upper() if not chainId.isupper() else chainId
        secName = nameSpace.name[0] if nameSpace.name else ''
        factory = AccountFactory(chainId)
        account = factory.create()
        Config.writeToFile(chainId, account, secName, parser)

    elif vars(nameSpace)['subparser-name-accounts'] == 'list':
        chainId = nameSpace.network[0] if nameSpace.network else 'L'
        chainId = chainId.upper() if not chainId.isupper() else chainId
        Config.printListAccounts(chainId, parser)



    elif vars(nameSpace)['subparser-name-accounts'] == 'set-default':
        Config.setDefaultAccount(nameSpace.address[0], parser)

    elif vars(nameSpace)['subparser-name-accounts'] == 'remove':
        Config.removeAccount(nameSpace.address[0], parser)

    elif vars(nameSpace)['subparser-name-accounts'] == 'show':
        Config.show(nameSpace.address[0], parser)

    elif vars(nameSpace)['subparser-name-accounts'] == 'seed':
        chainId = nameSpace.network[0] if nameSpace.network else 'L'
        if not (chainId.isalpha() and len(chainId) == 1):
            parser.error('The --network parameter accepts only CHAR type')
        chainId = chainId.upper() if not chainId.isupper() else chainId
        secName = nameSpace.name[0] if nameSpace.name else ''
        factory = AccountFactory(chainId)
        seed = nameSpace.stdin.read().splitlines() if not sys.stdin.isatty() else []
        if not seed:
            parser.error("Seed missing, type 'lto accounts seed --help' for instructions")
        account = factory.createFromSeed(seed[0])
        Config.writeToFile(chainId, account, secName, parser)

    else:
        parser.error('Type lto accounts --help for instructions')
