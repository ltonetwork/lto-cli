# LTO Network CLI client

### Manage accounts

```
lto accounts create
lto accounts seed --name foobar <<< "my seed"
lto accounts list
lto accounts set-default foobar
lto accounts remove 3JuijVBB7NCwCz2Ae5HhCDsqCXzeBLRTyeL
```

### Transactions

```
lto tx transfer --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --amount 1000000000
```

### Public node

```
lto config-node url https://nodes.lto.network
lto broadcast
```

### Common options

```
--network CHAINID
--account NAME|ADDRESS
```
