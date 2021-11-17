from configparser import ConfigParser
from lto.accounts.ed25519.account_ed25519 import AccountED25519 as Account

import base58
from nacl.signing import SigningKey, VerifyKey
import os
from pathlib import Path

CHAIN_ID = 'L'
DEFAULT_URL_MAINNET = 'https://nodes.lto.network'
DEFAULT_URL_TESTNET = 'https://testnet.lto.network'
path = Path.joinpath(Path.home(), 'lto')

def write_to_file(chain_id, account, sec_name, parser):
    relative_path = Path.joinpath(path, chain_id)

    if not os.path.exists(relative_path):
        os.mkdir(relative_path)

    if not sec_name:
        sec_name = account.address

    config = ConfigParser()
    config.read(Path.joinpath(relative_path, 'Accounts.ini'))

    if not config.sections() and not find_account(address=account.address, name=sec_name):
        config.add_section(sec_name)
        config.set(sec_name, 'Address', account.address)
        config.set(sec_name, 'Public_key', base58.b58encode(account.public_key.__bytes__()))
        config.set(sec_name, 'Private_key', base58.b58encode(account.private_key.__bytes__()))
        config.set(sec_name, 'Seed', account.seed)
        config.write(open(Path.joinpath(relative_path, 'Accounts.ini'), 'w'))
        print(account.address)
        write_default_account(account, chain_id)

    else:
        if not find_account(address=account.address, name=sec_name):
            config.add_section(sec_name)
            config.set(sec_name, 'Address', account.address)
            config.set(sec_name, 'public_key', base58.b58encode(account.public_key.__bytes__()))
            config.set(sec_name, 'private_key', base58.b58encode(account.private_key.__bytes__()))
            config.set(sec_name, 'Seed', account.seed)
            config.write(open(Path.joinpath(relative_path, 'Accounts.ini'), 'w'))
            print(account.address)
            write_default_account(account, chain_id)
        else:
            parser.error("An account with the same id is already present, type 'lto accounts create --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")

# returns false if the account is not found, else returns the seed and the chain_id
def find_account(address = '', name = ''):
    directories = next(os.walk(path), (None, None, []))[1]
    for chain_id in directories:
        if 'Accounts.ini' in next(os.walk(Path.joinpath(path, chain_id)), (None, None, []))[2]:
            config = ConfigParser()
            config.read(Path.joinpath(path, '{}/Accounts.ini'.format(chain_id)))
            value = find_account_in_config(config, address, name)
            if value != False:
                return value, chain_id
    return False


def find_account_in_config(config, address='', name=''):
    for sec in config.sections():
        if address == config.get(sec, 'address') or name == sec:
            seed = config.get(sec, 'seed')
            private_key = config.get(sec, 'private_key')
            public_key = config.get(sec, 'public_key')
            address = config.get(sec, 'address')
            return [seed, private_key, public_key, address]
    return False


#  Change is set to false, so it won't change the predetermined default account
def write_default_account(account, chain_id, change=False):

    local_path = Path.joinpath(path, '{}/config.ini'.format(chain_id))
    config = ConfigParser()
    config.read(local_path)
    if not config.sections():
        config.add_section('Default')
        config.set('Default', 'Address', account.address)
        if chain_id == 'L':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_MAINNET)
        elif chain_id == 'T':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_TESTNET)
        config.write(open(local_path, 'w'))
    else:
        if not 'Default' in config.sections():
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(local_path, 'w'))
        elif change:
            config.remove_section('Default')
            config.add_section('Default')
            config.set('Default', 'Address', account.address)
            config.write(open(local_path, 'w'))

def list_accounts(chain_id, parser):
    list = []
    local_path = Path.joinpath(path, "{}/accounts.ini".format(chain_id))
    if not os.path.exists(local_path):
        parser.error("No account found for {} network, type 'lto accounts --help' for instructions".format(chain_id))
    else:
        config = ConfigParser()
        config.read(local_path)
        for section in config.sections():
            list.append([section , config.get(section, 'address')])
    return list

def det_default_addr_from_chain_id(chain_id):
    local_path = Path.joinpath(path, "{}/config.ini".format(chain_id))
    config = ConfigParser()
    config.read(local_path)
    if not 'Default' in config.sections():
        return ''
    else:
        return config.get('Default', 'address')

def print_list_accounts(chain_id, parser):
    list_acc = list_accounts(chain_id, parser)
    address = det_default_addr_from_chain_id(chain_id)


    for account in list_acc:
        temp = ' * {}'.format(account[1]) if account[1] == address else '   {}'.format(account[1])
        if not account[0] == account[1]:
            print(temp, " - ", account[0])
        else:
            print(temp)


def list_accounts_complete():
    list = []
    directories = next(os.walk(path), (None, None, []))[1]
    for chain_id in directories:
        if 'Accounts.ini' in next(os.walk(Path.joinpath(path, chain_id)), (None, None, []))[2]:
            config = ConfigParser()
            config.read(Path.joinpath(path, '{}/Accounts.ini'.format(chain_id)))
            list.append([chain_id, config.sections()])
    return list

def check_directory(dir=''):
    if not os.path.exists(Path.joinpath(path, dir)):
        os.mkdir(Path.joinpath(path, dir))

def set_default_accounts(name, parser):
    value = find_account(name=name)
    if not value:
        parser.error(
            "No account found with this id, type 'lto accounts create --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")
    else:
        account = Account(seed=value[0][0], private_key=value[0][1], public_key=value[0][2], address=value[0][3])
        write_default_account(account, value[1], change=True)

def remove_account(name, parser):
    value = find_account(name=name)
    if not value:
        parser.error(
            "No account found with this id, type 'lto accounts remove --help' for instructions or 'lto accounts list' to visualize the previously stored accounts")
    else:
        config = ConfigParser()
        config.read(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])))  # value[1] = chain_id
        address = config.get(name, 'address')
        config.remove_section(name)
        config.write(open(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])), 'w'))
        remove_default_account(address, value[1])
        delete_if_empty(Path.joinpath(path, '{}/Accounts.ini'.format(value[1])))

def delete_if_empty(path_delete):
    config = ConfigParser()
    config.read(path_delete)
    if not config.sections():
        os.remove(path_delete)


def remove_default_account(address, chain_id):
    config = ConfigParser()
    config.read(Path.joinpath(path, '{}/config.ini'.format(chain_id)))
    if 'Default' in config.sections():
        if address == config.get('Default', 'address'):
            config.remove_section('Default')
            config.write(open(Path.joinpath(path, '{}/config.ini'.format(chain_id)), 'w'))
            delete_if_empty(Path.joinpath(path, '{}/config.ini'.format(chain_id)))

def set_node(name_space, parser):
    chain_id = name_space.network[0] if name_space.network else 'L'
    if not (chain_id.isalpha() and len(chain_id) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    chain_id = chain_id.upper() if not chain_id.isupper() else chain_id
    node = name_space.url[0]
    check_directory(chain_id)
    config = ConfigParser()
    config.read(Path.joinpath(path, '{}/config.ini'.format(chain_id)))
    if not 'Node' in config.sections():
        config.add_section('Node')
    config.set('Node', 'url', node)
    config.write(open(Path.joinpath(path, '{}/config.ini'.format(chain_id)), 'w'))

def show(id, parser):
    value = find_account(address=id, name=id)
    if not value:
        parser.error("No matching account fo {}, type 'lto accounts --help' for instructions")
    else:
        if id != value[0][3]:
            print('Name    : ', id)
        print('Address : ', value[0][3])
        print('Sign    :')
        print('   SecretKey  : ',value[0][1] )
        print('   public_key  : ',value[0][2] )
        print('Seed    : ', value[0][0])

