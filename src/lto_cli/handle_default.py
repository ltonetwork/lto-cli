from configparser import ConfigParser
from pathlib import Path
import json
import os

from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto_cli import config as Config
from lto.public_node import PublicNode


CHAIN_ID = 'L'
URL = 'https://nodes.lto.network'

path = Path.joinpath(Path.home(), '.lto')

def pretty_print(transaction):
    print(json.dumps(transaction.to_json(), indent=2))

def get_node(chain_id, parser):
    local_path = Path.joinpath(path, "{}/config.ini".format(chain_id))
    if not os.path.exists(local_path):
        parser.error("No account found for {} network, type 'lto account --help' for instructions".format(chain_id))
    config = ConfigParser()
    config.read(local_path)
    if not 'Node' in config.sections():
        parser.error("No node set for this network, type 'lto set-node --help' for instructions")
    else:
        return PublicNode(config.get('Node', 'url'))


def get_account(chain_id, parser, name=''):
    local_path = Path.joinpath(path, "{}/accounts.ini".format(chain_id))

    if not os.path.exists(local_path):
        parser.error("No account found for {} network, type 'lto account --help' for instructions".format(chain_id))

    config = ConfigParser()
    config.read(local_path)
    if name:
        if not name in config.sections():
            parser.error("No account found for {} network with name {}, use 'lto account list' to see all accounts".format(chain_id, name))
        elif 'seed' in config[name]:
            return AccountFactory(chain_id).create_from_seed(config.get(name, 'seed'))
        elif 'private_key' in config[name]:
            return AccountFactory(chain_id).create_from_private_key(config.get(name, 'private_key'))
        elif 'public_key' in config[name]:
            return AccountFactory(chain_id).create_from_public_key(config.get(name, 'public_key'))
        else:
            parser.error("Invalid settings of account {}".format(name))
    else:
        local_path = Path.joinpath(path, "{}/config.ini".format(chain_id))
        if not os.path.exists(local_path):
            parser.error("No Default account set, type 'lto account set-default --help' for instructions".format(chain_id))
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


def check(chain_id, parser):
    if not (chain_id.isalpha() and len(chain_id) == 1):
        parser.error('The --network parameter accepts only CHAR type')
    return chain_id.upper() if not chain_id.isupper() else chain_id

