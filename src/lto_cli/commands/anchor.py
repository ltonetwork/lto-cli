from lto_cli import handle_default as handle
from lto.transactions.anchor import Anchor
import select
import hashlib
from lto import crypto

algorithms = {
    'sha256': hashlib.sha256,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
    'blake2b': hashlib.blake2b,
    'blake2s': hashlib.blake2s,
    'sha3_224': hashlib.sha3_224,
    'sha3_256': hashlib.sha3_256,
    'sha3_384': hashlib.sha3_384,
    'sha3_512': hashlib.sha3_512,
}

def func(name_space, parser):
    hash = vars(name_space)['hash'][0] if vars(name_space)['hash'] else None
    algo = vars(name_space)['algo'][0] if vars(name_space)['algo'] else None
    encoding = vars(name_space)['encoding'][0] if vars(name_space)['encoding'] else ''
    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None
    unsigned = vars(name_space)['unsigned']
    no_broadcast = vars(name_space)['no_broadcast']

    data = None
    if select.select([name_space.stdin, ], [], [], 0.0)[0]:
        data = name_space.stdin.read()

    if data and hash:
        parser.error("Hash can be uploaded from standard input or by using the --hash option, not both")
    if encoding and not hash:
        parser.error("Encoding is an option of the --hash command")
    if hash and algo:
        parser.error("Algorithm is an option accessible only if there is a file input")
    if encoding not in ['', 'base58', 'base64']:
        parser.error("Unrecognized encoding format, please use base58 or base64 encoding")
    if algo and algo not in algorithms:
        parser.error("Unsupported hashing algorithm")
    if unsigned and not no_broadcast:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor "
            "--help' for more information")

    if data:
        method = algorithms[algo] if algo else hashlib.sha256
        hash = method(crypto.str2bytes(data)).hexdigest()

    if encoding:
        decoded_hash = crypto.decode(hash, encoding)
        transaction = Anchor(decoded_hash)
    else:
        decoded_hash = crypto.decode(hash, 'hex')
        transaction = Anchor(decoded_hash)

    if not unsigned:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if sponsor:
            transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
        if not no_broadcast:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))

    handle.pretty_print(transaction)


