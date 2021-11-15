from configparser import ConfigParser
from LTO.Account import Account

import base58
from nacl.signing import SigningKey, VerifyKey
import os
from pathlib import Path

CHAIN_ID = 'L'
DEFAULT_URL_MAINNET = 'https://nodes.lto.network'
DEFAULT_URL_TESTNET = 'https://testnet.lto.network'
path = Path.joinpath(Path.home(), 'lto')

def writeToFile(chainId, account, secName, parser):
    relativePath = Path.joinpath(path, chainId)

    if not os.path.exists(relativePath):
        os.mkdir(relativePath)

    if not secName:
        secName = account.address

    config = ConfigParser()
    config.read(Path.joinpath(relativePath, 'Accounts.ini'))

    if not config.sections() and not findAccount(address=account.address, name=secName):
        config.add_section(secName)
        config.set(secName, 'Address', account.address)
        config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
        config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
        config.set(secName, 'Seed', account.seed)
        config.write(open(Path.joinpath(relativePath, 'Accounts.ini'), 'w'))
        print(account.address)
        writeDefaultAccount(account, chainId)

    else:
        if not findAccount(address=account.address, name=secName):
            config.add_section(secName)
            config.set(secName, 'Address', account.address)
            config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
            config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
            config.set(secName, 'Seed', account.seed)
            config.write(open(Path.joinpath(relativePath, 'Accounts.ini'), 'w'))
            print(account.address)
            writeDefaultAccount(account, chainId)
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
def writeDefaultAccount(account, chainId, change=False):

    localPath = Path.joinpath(path, '{}/config.ini'.format(chainId))
    config = ConfigParser()
    config.read(localPath)
    if not config.sections():
        config.add_section('Default')
        config.set('Default', 'Address', account.address)
        if chainId == 'L':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_MAINNET)
        elif chainId == 'T':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_TESTNET)
        config.write(open(localPath, 'w'))
    else:
        if not 'Default' in config.sections():
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(localPath, 'w'))
        elif change:
            config.remove_section('Default')
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(localPath, 'w'))

def listAccounts(chainId, parser):
    list = []
    localPath = Path.joinpath(path, "{}/accounts.ini".format(chainId))
    if not os.path.exists(localPath):
        parser.error("No account found for {} network, type 'lto accounts --help' for instructions".format(chainId))
    else:
        config = ConfigParser()
        config.read(localPath)
        for section in config.sections():
            list.append([section , config.get(section, 'address')])
    return list

def getDefaultAddrFromChainId(chainId):
    localPath = Path.joinpath(path, "{}/config.ini".format(chainId))
    config = ConfigParser()
    config.read(localPath)
    if not 'Default' in config.sections():
        return ''
    else:
        return config.get('Default', 'address')

def printListAccounts(chainId, parser):
    listAcc = listAccounts(chainId, parser)
    address = getDefaultAddrFromChainId(chainId)


    for account in listAcc:
        temp = ' * {}'.format(account[1]) if account[1] == address else '   {}'.format(account[1])
        if not account[0] == account[1]:
            print(temp, " - ", account[0])
        else:
            print(temp)


def listAccountsComplete():
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
        writeDefaultAccount(account, value[1], change=True)

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
        removeDefaultAccount(address, value[1])
        deleteIfEmpty(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])))

def deleteIfEmpty(pathDelete):
    config = ConfigParser()
    config.read(pathDelete)
    if not config.sections():
        os.remove(pathDelete)


def removeDefaultAccount(address, chainId):
    config = ConfigParser()
    config.read(Path.joinpath(path, '{}/config.ini'.format(chainId)))
    if 'Default' in config.sections():
        if address == config.get('Default', 'address'):
            config.remove_section('Default')
            config.write(open(Path.joinpath(path, '{}/config.ini'.format(chainId)), 'w'))
            deleteIfEmpty(Path.joinpath(path, '{}/config.ini'.format(chainId)))

def setNode(nameSpace, parser):
    chainId = nameSpace.network[0] if nameSpace.network else 'L'
    if not (chainId.isalpha() and len(chainId) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    chainId = chainId.upper() if not chainId.isupper() else chainId
    node = nameSpace.url[0]
    checkDirectory(chainId)
    config = ConfigParser()
    config.read(Path.joinpath(path, '{}/config.ini'.format(chainId)))
    if not 'Node' in config.sections():
        config.add_section('Node')
    config.set('Node', 'url', node)
    config.write(open(Path.joinpath(path, '{}/config.ini'.format(chainId)), 'w'))

def show(id, parser):
    value = findAccount(address=id, name=id)
    if not value:
        parser.error("No matching account fo {}, type 'lto accounts --help' for instructions")
    else:
        if id != value[0][3]:
            print('Name    : ', id)
        print('Address : ', value[0][3])
        print('Sign    :')
        print('   SecretKey  : ',value[0][1] )
        print('   PublicKey  : ',value[0][2] )
        print('Seed    : ', value[0][0])

