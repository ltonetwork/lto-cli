from configparser import ConfigParser
from pathlib import Path
import json
import os

from LTO.AccountFactory import AccountFactory
from LTOCli import Config
from LTO.PublicNode import PublicNode


CHAIN_ID = 'L'
URL = 'https://nodes.lto.network'
#path = Path.home()

path = Path.joinpath(Path.home(), 'lto')

def prettyPrint(transaction):
    print(json.dumps(transaction.toJson(), indent=2))

def getNode():
    global URL
    config = ConfigParser()
    localPath = Path.joinpath(path, 'Default/config.ini')

    if not os.path.exists(localPath):
        return PublicNode(URL)
    else:
        config.read(localPath)
        if not 'Node' in config.sections():
            return PublicNode(URL)
        else:
            return PublicNode(config.get('Node', 'url'))

def getDefaultAccount(parser):
    relativePath = Path.joinpath(path, 'Default/config.ini')
    if not os.path.exists(relativePath):
        parser.error("No Default account set, type 'lto accounts set-default --help' for instructions")
    else:
        config = ConfigParser()
        config.read(relativePath)
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

def getAccountFromName(name, parser):
    value = Config.findAccount(address=name, name = name)
    if not value:
        parser.error("No matching account found, type 'lto accounts --help' for information on how to create an "
                     "account, or 'lto accounts list' for a list of all locally stored accounts")
    else:
        return AccountFactory(value[1]).createFromSeed(value[0][0])


