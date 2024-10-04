from configparser import ConfigParser
from lto.accounts.ed25519.account_ed25519 import AccountED25519 as Account

import base58
import os
from pathlib import Path

DEFAULT_URL_MAINNET = 'https://nodes.lto.network'
DEFAULT_URL_TESTNET = 'https://testnet.lto.network'
path = Path.joinpath(Path.home(), '.lto')


def write_to_file(chain_id, account, sec_name, parser):
    relative_path = Path.joinpath(path, chain_id)

    if not os.path.exists(relative_path):
        os.mkdir(relative_path)

    if not sec_name:
        sec_name = account.address

    config = ConfigParser()
    config.read(Path.joinpath(relative_path, 'accounts.ini'))

    if find_account_in_config(config=config, address=account.address, name=sec_name):
        parser.error("An account with the same id is already present, type 'lto account create --help' for instructions or 'lto account list' to visualize the previously stored accounts")

    config.add_section(sec_name)
    config.set(sec_name, 'Address', account.address)
    config.set(sec_name, 'Public_key', base58.b58encode(account.public_key.__bytes__()))
    config.set(sec_name, 'Private_key', base58.b58encode(account.private_key.__bytes__()))
    config.set(sec_name, 'Seed', account.seed)
    if account.nonce != 0:
        config.set(sec_name, 'Nonce', str(account.nonce))
    config.write(open(Path.joinpath(relative_path, 'accounts.ini'), 'w'))
    write_default_account(account, chain_id)


def find_account_in_config(config, address='', name=''):
    for sec in config.sections():
        if address == config.get(sec, 'address') or name == sec or name == config.get(sec, 'address'):
            seed = config.get(sec, 'seed', fallback = '')
            nonce = config.get(sec, 'nonce', fallback = '0')
            private_key = config.get(sec, 'private_key', fallback = '')
            public_key = config.get(sec, 'public_key')
            address = config.get(sec, 'address')
            return [seed, private_key, public_key, address, int(nonce)]
    return False


#  Change is set to false, so it won't change the predetermined default account
def write_default_account(account, chain_id, change=False):
    local_path = Path.joinpath(path, chain_id, 'config.ini')
    config = ConfigParser()
    config.read(local_path)
    if not config.sections():
        if chain_id == 'L':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_MAINNET)
        elif chain_id == 'T':
            config.add_section('Node')
            config.set('Node', 'url', DEFAULT_URL_TESTNET)

    if 'Default' in config.sections():
        if not change:
            return
        config.remove_section('Default')

    config.add_section('Default')
    config.set('Default', 'Address', account.address)
    config.write(open(local_path, 'w'))


def list_accounts(chain_id, parser):
    list = []
    local_path = Path.joinpath(path, chain_id, "accounts.ini")
    if not os.path.exists(local_path):
        parser.error(f"No account found for {chain_id} network, type 'lto account --help' for instructions")
    else:
        config = ConfigParser()
        config.read(local_path)
        for section in config.sections():
            list.append([section, config.get(section, 'address')])
    return list


def get_default_addr_from_chain_id(chain_id):
    local_path = Path.joinpath(path, chain_id, "config.ini")
    config = ConfigParser()
    config.read(local_path)
    if not 'Default' in config.sections():
        return ''
    else:
        return config.get('Default', 'address')


def print_list_accounts(chain_id, parser):
    list_acc = list_accounts(chain_id, parser)
    address = get_default_addr_from_chain_id(chain_id)

    for account in list_acc:
        temp = (' * %s' if account[1] == address else '   %s') % account[1]
        if not account[0] == account[1]:
            print(temp, " - ", account[0])
        else:
            print(temp)


def check_directory(dir=''):
    if not os.path.exists(Path.joinpath(path, dir)):
        os.mkdir(Path.joinpath(path, dir))


def set_default_accounts(chain_id, name, parser):
    config = get_config_from_chain_id(chain_id)
    value = find_account_in_config(config, name=name)
    if not value:
        parser.error("No account found with this id, type 'lto account create --help' for instructions or 'lto account list' to visualize the previously stored accounts")

    account = Account(seed=value[0], private_key=value[1], public_key=value[2], address=value[3])
    write_default_account(account, chain_id, change=True)


def remove_account(chain_id, name, parser):
    config = get_config_from_chain_id(chain_id)
    value = find_account_in_config(config, name=name)

    if not value:
        parser.error("No account found with this id, type 'lto account remove --help' for instructions or 'lto account list' to visualize the previously stored accounts")

    config.remove_section(get_section_name_from_address(config, value[3]))
    config.write(open(Path.joinpath(path, chain_id, 'accounts.ini'), 'w'))
    remove_default_account(value[3], chain_id)
    delete_if_empty(Path.joinpath(path, chain_id, 'accounts.ini'))


def delete_if_empty(path_delete):
    config = ConfigParser()
    config.read(path_delete)
    if not config.sections():
        os.remove(path_delete)


def remove_default_account(address, chain_id):
    config_file = Path.joinpath(path, chain_id, 'config.ini')
    config = ConfigParser()
    config.read(config_file)
    if 'Default' in config.sections():
        if address == config.get('Default', 'address'):
            config.remove_section('Default')
            config.write(open(config_file, 'w'))
            delete_if_empty(config_file)


def set_node(name_space, parser):
    chain_id = name_space.network[0] if name_space.network else 'L'
    if not (chain_id.isalpha() and len(chain_id) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    chain_id = chain_id.upper() if not chain_id.isupper() else chain_id
    node = name_space.url[0]
    check_directory(chain_id)
    config = ConfigParser()
    config.read(Path.joinpath(path, chain_id, 'config.ini'))
    if not 'Node' in config.sections():
        config.add_section('Node')
    config.set('Node', 'url', node)
    config.write(open(Path.joinpath(path, chain_id, 'config.ini'), 'w'))


def show(chain_id, id, parser):
    config = get_config_from_chain_id(chain_id)
    value = find_account_in_config(config, address=id, name=id)

    if not value:
        network = 'mainnet' if chain_id == 'L' else 'testnet' if chain_id == 'T' else f"network {chain_id}"
        network_opt = '' if chain_id == 'L' else ' -T' if chain_id == 'T' else f" --network={chain_id}"
        parser.error(f"No account '{id}' on {network}. Type 'lto account list{network_opt}' to list all accounts on {network}")

    print('Name        :', id) if id != value[3] else None
    print('Address     :', value[3])
    print('Public key  :', value[2])
    print('Private key :', value[1] or '[unknown]')
    print('Seed        :', value[0] or '[unknown]')
    if value[4]:
        print('Nonce       :', str(value[4]))

def get_config_from_chain_id(chain_id):
    config_file = Path.joinpath(path, chain_id, 'accounts.ini')
    config = ConfigParser()
    config.read(config_file)
    return config

def get_section_name_from_address(config, address):
    sections = config.sections()
    for sec in sections:
        if config.get(sec, 'address') == address:
            return sec
    return None
