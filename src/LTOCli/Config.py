import configparser
from LTO.Account import Account
import base58
from nacl.signing import SigningKey, VerifyKey
import os
from pathlib import Path

CHAIN_ID = 'L'
path = Path.home()


def writeToFile(path_, account, secName, parser):
    path_ = 'lto/' + path_
    error = 'Name'
    if not secName:
        secName = account.address
        error = 'Address'
    config = configparser.ConfigParser()
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
    config = configparser.ConfigParser()
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
    config = configparser.ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    if name not in config.sections():
        config.read('{}/lto/T/accounts.ini'.format(path))
        if name not in config.sections():
            parser.error("The account needs to be createed first, type 'lto accounts create --help' for instructions ")
        else:
            address = config.get(name, 'address')
            chainId = 'T'
    else:
        address = config.get(name, 'address')
        chainId = 'L'
    return address, chainId


def setDefaultAccount(name, parser, address='', chainId=''):
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


def listAccounts():
    config = configparser.ConfigParser()
    config.read('{}/lto/L/accounts.ini'.format(path))
    listL = config.sections()
    config.clear()
    config.read('{}/lto/T/accounts.ini'.format(path))
    listT = config.sections()
    return listL, listT


def getNewDefault(parser):
    config = configparser.ConfigParser()
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
    config = configparser.ConfigParser()
    config.read('{}/lto/L/config.ini'.format(path))
    if 'Default' in config.sections():
        if config.get('Default', 'account') == address:
            config.remove_section('Default')
            config.write(open('{}/lto/L/config.ini'.format(path), 'w'))
            # getNewDefault()


def removeAccount(name, parser):
    # check into the L directory
    config = configparser.ConfigParser()
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


def checkDirectory():
    if not os.path.exists(path='{}/lto'.format(path)):
        os.mkdir(path='{}/lto'.format(path))
        os.mkdir(path='{}/lto/L'.format(path))
        os.mkdir(path='{}/lto/T'.format(path))
    else:
        if not os.path.exists(path='{}/lto/L'.format(path)):
            os.mkdir(path='{}/lto/L'.format(path))
        if not os.path.exists(path='{}/lto/T'.format(path)):
            os.mkdir(path='{}/lto/T'.format(path))

