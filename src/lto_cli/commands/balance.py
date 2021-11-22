from lto_cli import handle_default as handle
from lto.public_node import PublicNode

def func(name_space, parser):
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    node = PublicNode(handle.get_node(chain_id, parser))