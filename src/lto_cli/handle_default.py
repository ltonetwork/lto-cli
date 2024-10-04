from configparser import ConfigParser
from pathlib import Path
import json
import os

from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.crypto import validate_address as lto_validate_address

from lto_cli import config as Config
from lto.public_node import PublicNode


CHAIN_ID = 'L'
URL = 'https://nodes.lto.network'

path = Path.joinpath(Path.home(), '.lto')

def pretty_print(transaction):
    print(json.dumps(transaction.to_json(), indent=2))

def get_node(chain_id, parser):
    local_path = Path.joinpath(path, f"{chain_id}/config.ini")
    if not os.path.exists(local_path):
        parser.error(f"No account found for {chain_id} network, type 'lto account --help' for instructions")
    config = ConfigParser()
    config.read(local_path)
    if not 'Node' in config.sections():
        parser.error("No node set for this network, type 'lto set-node --help' for instructions")
    else:
        return PublicNode(config.get('Node', 'url'))


def get_account(chain_id, parser, name=''):
    local_path = Path.joinpath(path, f"{chain_id}/accounts.ini")

    if not os.path.exists(local_path):
        network = 'mainnet' if chain_id == 'L' else 'testnet' if chain_id == 'T' else f"network {chain_id}"
        parser.error(f"No accounts for {network}")

    config = ConfigParser()
    config.read(local_path)
    if name:
        if not name in config.sections():
            network = 'mainnet' if chain_id == 'L' else 'testnet' if chain_id == 'T' else f"network {chain_id}"
            network_opt = '' if chain_id == 'L' else ' -T' if chain_id == 'T' else f" --network={chain_id}"
            parser.error(f"No account '{name}' on {network}. Type 'lto account list{network_opt}' to list all accounts on {network}")
        elif 'seed' in config[name]:
            return AccountFactory(chain_id).create_from_seed(config.get(name, 'seed'))
        elif 'private_key' in config[name]:
            return AccountFactory(chain_id).create_from_private_key(config.get(name, 'private_key'))
        elif 'public_key' in config[name]:
            return AccountFactory(chain_id).create_from_public_key(config.get(name, 'public_key'))
        else:
            parser.error(f"Invalid settings of account {name}")
    else:
        local_path = Path.joinpath(path, f"{chain_id}/config.ini")
        if not os.path.exists(local_path):
            parser.error("No Default account set, type 'lto account set-default --help' for instructions")
        config.clear()
        config.read(local_path)
        if not 'Default' in config.sections():
            parser.error("No Default account set, type 'lto account set-default --help' for instructions")
        else:
            address = config.get('Default', 'address')
            config.clear()
            config = Config.get_config_from_chain_id(chain_id)
            value = Config.find_account_in_config(config, address=address, name='')
            if not value:
                parser.error("Error with default account type 'lto account set-default --help' for instructions")
            else:
                return AccountFactory(chain_id).create_from_seed(value[0])


def get_address(chain_id, parser, account):
    return account if validate_address(account) or not account else get_account(chain_id, parser, account).address


def validate_address(address):
    try:
        lto_validate_address(address)
        return True
    except:
        return False


def check(chain_id, parser):
    if not (chain_id.isalpha() and len(chain_id) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    return chain_id.upper() if not chain_id.isupper() else chain_id

