from configparser import ConfigParser
from LTO.Account import Account

import base58
from nacl.signing import SigningKey, VerifyKey
import os
from pathlib import Path

CHAIN_ID = 'L'
#path = Path.home()
path = Path.joinpath(Path.home(), 'lto')

def writeToFile(chainId, account, secName, parser):
    relativePath = Path.joinpath(path, chainId)

    if not os.path.exists(relativePath):
        os.mkdir(relativePath)

    if not secName:
        secName = account.address

    config = ConfigParser()
    config.read(Path.joinpath(relativePath, 'Accounts.ini'))

    if not config.sections(): # the file is not present
        config.add_section(secName)
        config.set(secName, 'Address', account.address)
        config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
        config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
        config.set(secName, 'Seed', account.seed)
        config.write(open(Path.joinpath(relativePath, 'Accounts.ini'), 'w'))
        writeDefaultAccount(account)

    else:
        if not findAccount(address=account.address, name=secName):
            config.add_section(secName)
            config.set(secName, 'Address', account.address)
            config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
            config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
            config.set(secName, 'Seed', account.seed)
            config.write(open(Path.joinpath(relativePath, 'Accounts.ini'), 'w'))
            writeDefaultAccount(account)
        else:
            parser.error("An account with the same id is already present, type 'lto accounts create --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")

# returns false if the account is not found, else returns the seed and the chainID
def findAccount(address = '', name = ''):
    directories = next(os.walk(path), (None, None, []))[1]
    for chainId in directories:
        if 'Accounts.ini' in next(os.walk(Path.joinpath(path, chainId)), (None, None, []))[2]:
            config = ConfigParser()
            config.read(Path.joinpath(path, '{}/Accounts.ini'.format(chainId)))
            value = findAccountInConfig(config, address, name)
            if value != False:
                return value, chainId
    return False


def findAccountInConfig(config, address='', name=''):
    for sec in config.sections():
        if address == config.get(sec, 'address') or name == sec:
            seed = config.get(sec, 'seed')
            privateKey = config.get(sec, 'privateKey')
            publicKey = config.get(sec, 'publicKey')
            address = config.get(sec, 'address')
            return [seed, privateKey, publicKey, address]
    return False


#  Change is set to false, so it won't change the predetermined default account
def writeDefaultAccount(account, change = False):
    checkDirectory('Default')
    localPath = Path.joinpath(path,'Default/config.ini')
    config = ConfigParser()
    config.read(localPath)
    if not config.sections():
        config.add_section('Default')
        config.set('Default', 'Address', account.address)
        config.write(open(Path.joinpath(path,'Default/config.ini'), 'w'))
    else:
        if not 'Default' in config.sections():
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(Path.joinpath(path,'Default/config.ini'), 'w'))
        elif change:
            config.remove_section('Default')
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(Path.joinpath(path,'Default/config.ini'), 'w'))


def listAccounts():
    list = []
    directories = next(os.walk(path), (None, None, []))[1]
    for chainId in directories:
        if 'Accounts.ini' in next(os.walk(Path.joinpath(path, chainId)), (None, None, []))[2]:
            config = ConfigParser()
            config.read(Path.joinpath(path, '{}/Accounts.ini'.format(chainId)))
            list.append([chainId, config.sections()])
    return list

def checkDirectory(dir=''):
    if not os.path.exists(Path.joinpath(path, dir)):
        os.mkdir(Path.joinpath(path, dir))

def setDefaultAccount(name, parser):
    value = findAccount(name=name)
    if not value:
        parser.error(
            "No account found with this id, type 'lto accounts create --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")
    else:
        account = Account(seed=value[0][0], privateKey=value[0][1], publicKey=value[0][2], address=value[0][3])
        writeDefaultAccount(account, change=True)

def removeAccount(name, parser):
    value = findAccount(name=name)
    if not value:
        parser.error(
            "No account found with this id, type 'lto accounts remove --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")
    else:
        config = ConfigParser()
        config.read(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])))  # value[1] = chainId
        address = config.get(name, 'address')
        config.remove_section(name)
        config.write(open(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])), 'w'))
        removeDefaultAccount(address)

def removeDefaultAccount(address):
    config = ConfigParser()
    config.read(Path.joinpath(path, 'Default/config.ini'))
    if 'Default' in config.sections():
        if address == config.get('Default', 'address'):
            config.remove_section('Default')
            config.write(open(Path.joinpath(path, 'Default/config.ini'), 'w'))

def setNode(nameSpace):
    node = nameSpace.url[0]
    checkDirectory('Default')
    config = ConfigParser()
    config.read(Path.joinpath(path, 'Default/config.ini'))
    if not 'Node' in config.sections():
        config.add_section('Node')
    config.set('Node', 'url', node)
    config.write(open(Path.joinpath(path, 'Default/config.ini'), 'w'))
