from lto_cli import config
from lto_cli import handle_default as handle

def func(name_space, parser):
    if vars(name_space)['subparser-name-node'] == 'show':
        chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
        print(handle.get_node(chain_id, parser).url)
    elif vars(name_space)['subparser-name-node'] == 'set':
        config.set_node(name_space, parser)
    elif vars(name_space)['subparser-name-node'] == 'status':
        chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
        node = handle.get_node(chain_id, parser)
        status = node.node_status()

        print('Blockchain Height  : ', status['blockchainHeight'])
        print('State Height       : ', status['stateHeight'])
        print('Updated Timestamp  : ', status['updatedTimestamp'])
        print('Updated Date       : ', status['updatedDate'])

    else:
        parser.error('Type "lto node --help" for instructions')
    #config.set_node(name_space, parser)