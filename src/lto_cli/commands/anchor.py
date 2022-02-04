from lto_cli import handle_default as handle
from lto.transactions.anchor import Anchor
from lto import crypto
import select
import hashlib
from lto import crypto
import sys
import os


def func(name_space, parser):
    # Need to make a flowChart for this
    hash = vars(name_space)['hash'][0] if vars(name_space)['hash'] else None
    algo = vars(name_space)['algo'][0] if vars(name_space)['algo'] else None
    encoding = vars(name_space)['encoding'][0] if vars(name_space)['encoding'] else ''
    data = None
    if select.select([name_space.stdin, ], [], [], 0.0)[0]:
        data = name_space.stdin.read()


    if data and hash:
        parser.error("Hash can be uploaded from standard input or by using the --hash option, not both")
    if encoding and not hash:
        parser.error("Encoding is an option of the --hash command")
    if hash and algo:
        parser.error("Algorithm is an option accessible only if there is a file input")

    algorithsm = {
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
    if algo and algo not in algorithsm:
        parser.error("Unsupported hashing algorithm")

    if data:
        if not algo:
            hash = algorithsm['sha256'](crypto.str2bytes(data)).hexdigest()
        else:
            hash = algorithsm[algo](crypto.str2bytes(data)).hexdigest()

    if encoding:
        if encoding not in ['base58', 'base64']:
            parser.error("Unrecognized encoding format, please use base58 or base64 encoding")
        encoded_hash = crypto.recode(hash, encoding, 'hex')
        transaction = Anchor(encoded_hash)
    else:
        transaction = Anchor(hash)

    chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
    account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
    sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None

    if vars(name_space)['unsigned'] is False:
        transaction.sign_with(handle.get_account(chain_id, parser, account_name))
        if sponsor:
            transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
        if vars(name_space)['no_broadcast'] is False:
            transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
    elif vars(name_space)['no_broadcast'] is False:
        parser.error(
            "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto anchor "
            "--help' for more informations ")
    handle.pretty_print(transaction)


