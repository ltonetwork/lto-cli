from configparser import ConfigParser
from pathlib import Path
import json
import os

from LTO.Accounts.AccountFactoryED25519 import AccountED25519 as AccountFactory
from LTOCli import Config
from LTO.PublicNode import PublicNode


CHAIN_ID = 'L'
URL = 'https://nodes.lto.network'

path = Path.joinpath(Path.home(), 'lto')

def prettyPrint(transaction):
    print(json.dumps(transaction.toJson(), indent=2))

def getNode(chainId, parser):
    localPath = Path.joinpath(path, "{}/config.ini".format(chainId))
    if not os.path.exists(localPath):
        parser.error("No account found for {} network, type 'lto accounts --help' for instructions".format(chainId))
    config = ConfigParser()
    config.read(localPath)
    if not 'Node' in config.sections():
        parser.error("No node set for this network, type 'lto set-node --help' for instructions")
    else:
        return PublicNode(config.get('Node', 'url'))


def getAccount(chainId, parser, name = ''):
    localPath = Path.joinpath(path, "{}/accounts.ini".format(chainId))

    if not os.path.exists(localPath):
        parser.error("No account found for {} network, type 'lto accounts --help' for instructions".format(chainId))

    config = ConfigParser()
    config.read(localPath)
    if name:
        if name in config.sections():
            return AccountFactory(chainId).createFromSeed(config.get(name, 'seed'))
        else:
            parser.error("No account found for {} network with name {}, type 'lto accounts --help' for instructions".format(chainId, name))
    else:
        localPath = Path.joinpath(path, "{}/config.ini".format(chainId))
        if not os.path.exists(localPath):
            parser.error("No account found for {} network, type 'lto accounts --help' for instructions".format(chainId))
        config.clear()
        config.read(localPath)
        if not 'Default' in config.sections():
            parser.error("No Default account set, type 'lto accounts set-default --help' for instructions")
        else:
            address = config.get('Default', 'address')
            value = Config.findAccount(address=address, name='')
            if not value:
                parser.error(
                    "Error with default account type 'lto accounts set-default --help' for instructions")
            else:
                return AccountFactory(value[1]).createFromSeed(value[0][0])


def check(chainId, parser):
    if not (chainId.isalpha() and len(chainId) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    return chainId.upper() if not chainId.isupper() else chainId


