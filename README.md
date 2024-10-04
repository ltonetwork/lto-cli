![LTO github readme](https://user-images.githubusercontent.com/100821/196711741-96cd4ba5-932a-4e95-b420-42d4d61c21fd.png)

# CLI client

## Installation

```
pip install lto-cli
```

[pip](https://pip.pypa.io/en/stable/) is the package installer for Python.

## Usage

```
lto --help
lto [command] --help
```

### Manage accounts

```
lto account create
read -s -p "Enter seed: " seed && echo $seed | lto account seed
lto account list
lto account set-default foobar
lto account remove 3JuijVBB7NCwCz2Ae5HhCDsqCXzeBLRTyeL
lto account show 3JuijVBB7NCwCz2Ae5HhCDsqCXzeBLRTyeL
```

### Public node

```
lto node set https://nodes.lto.network
lto node show
lto node status
```

### Broadcast

Takes as input a transaction, signs it and broadcast it to the network

```
echo $TX_JSON | lto broadcast
```

If the input transaction is already signed, a second signature is added, which can be used for a multisig smart account.
To broadcast a signed transaction without adding a second signature use `--unsigned`.

### Balance

Display the balances of the default address or if specified of a specific address
```
lto balance
lto balance 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK
```

## Transactions

### Anchor

```
lto anchor --hash d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35
lto anchor --hash FJKTv1un7qsnyKdwKez7B67JJp3oCU5ntCVXcRsWEjtg --encoding base58
cat somefile.txt | lto anchor --algo sha256
```

Anchor multiple hashes in one transaction by repeating `--hash`:
```
lto anchor --hash HASH1 --hash HASH2 --hash HASH3
```

#### Mapped Anchor

Create a mapped anchor by specifying a key/value pair, seperated by a `:` (double colon).

```
lto anchor --hash a10933ea8afa05af54bc2ed0c9780bbc7e2e69964b76dcc69992a3fce94f11c5:48dbb907e9777a49af2f824b41278f27ef1cc0de2a926b3da19cfca897c08416
```

### Associations

```
lto association issue --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --type 1 --subject e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
lto association revoke --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --type 1 --subject e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
lto association incoming
lto association outgoing
```

### Transfer

```
lto transfer --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --amount 742.6
```

### Mass-transfer

```
echo "3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj 742.6
3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz 2184.2" | lto mass-transfer
```

_Recipient/amount pairs are read from stdin._

### Leasing

```
lto lease create --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --amount 742.6
lto lease cancel --leaseid 6XmeG7SRWiw8pD6Uad6D9AAaY354v5TV6AJMhPpHMkqy
lto lease incoming
lto lease outgoing
```

### Sponsorship

```
lto sponsorship create --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK
lto sponsorship cancel --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK
lto sponsorship incoming
```

### Data

```
lto data set <<< '{"foo": "bar"}'
lto data get
lto data get 3Jvtrp1GZ7r5J8SXXFqeKyH9GE5Q78meHzN
lto data get --key foo
```


### Script

```
cat my_script | lto script 
```

## Common options

```
--network CHAINID
--account NAME|ADDRESS
--sponsor NAME|ADDRESS
--no-broadcast
--unsigned
```

#### `--network`

Use `--network T` or `-T` to use testnet instead of mainnet. You need to set up accounts specifically for testnet.

#### `--account`

Select one of the accounts configured during setup. The account can be referenced by name or address. The name is only known locally.
If this option is omitted, the default account is used.

#### `--sponsor`

Choose an account to sponsor the transaction. The sponsor will co-sign the transaction and pay the transaction fee.

#### `--no-broadcast`

Create and sign the transaction, but don't broadcast it to the node. The JSON will be outputted.

#### `--unsigned`

Create the transaction, but don't sign it. This option should only be used in combination with `--no-broadcast`.
