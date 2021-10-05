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

def checkDirectory(dir = path):
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

# ---------------------------------------------------------------------------------------------------

def writeToFile2(path_, account, secName, parser):
    path_ = 'lto/' + path_
    print(path_)
    error = 'Name'
    if not secName:
        secName = account.address
        error = 'Address'
    config = ConfigParser()
    if os.path.exists(Path.joinpath(path,path_)):
        config.read(Path.joinpath(path,path_))
        if not nameAlreadyPresent(secName):
            config.add_section(secName)
            config.set(secName, 'Address', account.address)
            config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
            config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
            config.set(secName, 'Seed', account.seed)
            config.write(open(Path.joinpath(path,path_), 'w'))
        else:
            parser.error("{} already present. type 'lto accounts --help' for instructions".format(error))
    else:
        if not nameAlreadyPresent(secName):
            config.add_section(secName)
            config.set(secName, 'Address', account.address)
            config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
            config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
            config.set(secName, 'Seed', account.seed)
            config.write(open(Path.joinpath(path,path_), 'w'))
        else:
            parser.error("{} already present. type 'lto accounts --help' for instructions".format(error))

    config.clear()
    if not os.path.exists('{}/lto/L/config.ini'.format(path)):
        setDefaultAccount(secName, parser, account.address)
    else:
        config.read('{}/lto/L/config.ini'.format(path))
        if 'Default' not in config.sections():
            setDefaultAccount(secName, parser, account.address)


def nameAlreadyPresent(name):
    config = ConfigParser()
    if os.path.exists('{}/lto/L/accounts.ini'.format(path)):
        config.read('{}/lto/L/accounts.ini'.format(path))
        if name in config.sections():
            return True
    config.clear()
    if os.path.exists('{}/lto/L/accounts.ini'.format(path)):
        config.read('{}/lto/L/accounts.ini'.format(path))
        if name in config.sections():
            return True
    return False


def getAddressFromName(name, parser):
    config = ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    if name not in config.sections():
        config.read('{}/lto/T/accounts.ini'.format(path))
        if name not in config.sections():
            parser.error("The account needs to be created first, type 'lto accounts create --help' for instructions ")
        else:
            address = config.get(name, 'address')
            chainId = 'T'
    else:
        address = config.get(name, 'address')
        chainId = 'L'
    return address, chainId


def setDefaultAccount2(name, parser, address='', chainId=''):
    if not address:
        address, chainId = getAddressFromName(name, parser)

    if not chainId:
        chainId = str(base58.b58decode(address))[6]
    config = configparser.ConfigParser()
    if os.path.exists('{}/lto/L/config.ini'.format(path)):
        config.read('{}/lto/L/config.ini'.format(path))
        if 'Node' in config.sections():
            savedChainId = config.get('Node', 'chainid')
            if savedChainId and savedChainId != chainId:
                print('Attention!, Account belongs to a different network than the stored one')
        else:
            config.add_section('Node')
            config.set('Node', 'chainId', chainId)
            if chainId == 'L':
                config.set('Node', 'url', 'https://nodes.lto.network')
            else:
                config.set('Node', 'url', 'https://testnet.lto.netowrk')
        if 'Default' not in config.sections():
            config.add_section('Default')
            config.set('Default', 'account', address)
        else:
            config.set('Default', 'account', address)

    else:
        config.add_section('Default')
        config.set('Default', 'account', address)
        config.add_section('Node')
        config.set('Node', 'chainId', chainId)
        if chainId == 'L':
            config.set('Node', 'url', 'https://nodes.lto.network')
        else:
            config.set('Node', 'url', 'https://testnet.lto.netowrk')
    config.write(open('{}/lto/L/config.ini'.format(path), 'w'))


'''def listAccounts():
    config = ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    listL = config.sections()
    config.clear()
    config.read('{}/lto/T/accounts.ini'.format(path))
    listT = config.sections()
    return listL, listT'''


def getNewDefault(parser):
    config = ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    if os.path.exists('{}/lto/L/accounts.ini'.format(path)) and config.sections() != []:
        sections = config.sections()
        address = config.get(sections[0], 'address')
        setDefaultAccount(name='placeholder', parser = parser, address=address)
    else:
        config.clear()
        config.read('{}/lto/T/accounts.ini'.format(path))
        if os.path.exists('{}/lto/L/accounts.ini'.format(path)) and config.sections() != []:
            sections = config.sections()
            address = config.get(sections[0], 'address')
            setDefaultAccount(name='placeholder',  parser=parser, address=address)


def removeDefault(address):
    config = ConfigParser()
    config.read('{}/lto/L/config.ini'.format(path))
    if 'Default' in config.sections():
        if config.get('Default', 'account') == address:
            config.remove_section('Default')
            config.write(open('{}/lto/L/config.ini'.format(path), 'w'))
            # getNewDefault()


def removeAccount2(name, parser):
    # check into the L directory
    config = ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    if not name in config.sections():
        # in case the name provided is an address of an account registered under a name
        secName = findAccountSection(name, config)
        if secName in config.sections():
            address = config.get(secName, 'address')
            config.remove_section(secName)
            config.write(open('{}/lto/L/accounts.ini'.format(path), 'w'))
            removeDefault(address)
        else:
            # check into the T directory
            config.clear()
            config.read('{}/lto/T/accounts.ini'.format(path))
            if not name in config.sections():
                secName = findAccountSection(name, config)
                if secName in config.sections():
                    address = config.get(secName, 'address')
                    config.remove_section(secName)
                    config.write(open('{}/lto/T/accounts.ini'.format(path), 'w'))
                    removeDefault(address)
                else:
                    parser.error("The account does not exist, type 'lto accounts create --help' for instructions ")

            else:
                address = config.get(name, 'address')
                config.remove_section(name)
                config.write(open('{}/lto/T/accounts.ini'.format(path), 'w'))
                removeDefault(address)
    else:
        address = config.get(name, 'address')
        config.remove_section(name)
        config.write(open('{}/lto/L/accounts.ini'.format(path), 'w'))
        removeDefault(address)


# it returns the account section name from the address provided
def findAccountSection(address, config):
    for sec in config.sections():
        if config.get(sec, 'address') == address:
            return sec
    return ''


def setnode(nameSpace):
    node = nameSpace.url[0]
    # network = chainID
    # node = url (https://...)

    flag = False

    if nameSpace.network:
        network = nameSpace.network[0]
    else:
        network = CHAIN_ID
        flag = True

    config = configparser.ConfigParser()
    if os.path.exists('{}/lto/L/config.ini'.format(path)):
        config.read('{}/lto/L/config.ini'.format(path))
        if 'Node' not in config.sections():
            config.add_section('Node')
            config.set('Node', 'ChainId', network)
            config.set('Node', 'URL', node)
        else:
            if flag == False:
                config.set('Node', 'ChainId', network)
            config.set('Node', 'URL', node)
    else:
        config.add_section('Node')
        config.set('Node', 'ChainId', network)
        config.set('Node', 'URL', node)
    config.write(open('{}/lto/L/config.ini'.format(path), 'w'))



