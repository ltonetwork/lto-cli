from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto_cli import config
from lto_cli import handle_default as handle


def func(name_space, parser):
    chain_id = name_space.network[0] if name_space.network else 'L'
    chain_id = chain_id.upper() if not chain_id.isupper() else chain_id

    if vars(name_space)['subparser-name-account'] == 'create':
        if not (chain_id.isalpha() and len(chain_id) == 1):
            parser.error('The --network parameter accepts only CHAR type')
        chain_id = chain_id.upper() if not chain_id.isupper() else chain_id
        sec_name = name_space.name[0] if name_space.name else ''
        factory = AccountFactory(chain_id)
        account = factory.create()
        config.write_to_file(chain_id, account, sec_name, parser)
        print(account.address)

    elif vars(name_space)['subparser-name-account'] == 'list':
        config.print_list_accounts(chain_id, parser)

    elif vars(name_space)['subparser-name-account'] == 'set-default':
        config.set_default_accounts(chain_id, name_space.address[0], parser)

    elif vars(name_space)['subparser-name-account'] == 'remove':
        address = name_space.address if name_space.address else None
        if not address:
            address = name_space.account[0] if name_space.account else handle.get_account(chain_id, parser).address
        config.remove_account(chain_id, address, parser)

    elif vars(name_space)['subparser-name-account'] == 'show':
        address = name_space.address if name_space.address else None
        if not address:
            address = name_space.account[0] if name_space.account else handle.get_account(chain_id, parser).address
        config.show(chain_id, address, parser)

    elif vars(name_space)['subparser-name-account'] == 'seed':
        if not (chain_id.isalpha() and len(chain_id) == 1):
            parser.error('The --network parameter accepts only CHAR type')
        sec_name = name_space.name[0] if name_space.name else ''
        factory = AccountFactory(chain_id)
        seed = name_space.stdin.read().splitlines()
        if not seed:
            parser.error("Seed missing, type 'lto account seed --help' for instructions")
        account = factory.create_from_seed(seed[0])
        config.write_to_file(chain_id, account, sec_name, parser)
        print(account.address)

    else:
        parser.error('Type lto account --help for instructions')
