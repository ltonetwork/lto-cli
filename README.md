# LTO Network CLI client

### Manage accounts

```
lto accounts create
lto accounts seed --name foobar <<< "my seed"
lto accounts list
lto accounts set-default foobar
lto accounts remove 3JuijVBB7NCwCz2Ae5HhCDsqCXzeBLRTyeL
```

### Public node

```
lto set-node --network L https://nodes.lto.network
```

### Anchor

```
lto anchor --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Associations

```
lto association issue --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --associationType 1 --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
lto association revoke --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --associationType 1 --hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Transfer

```
lto transfer --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --amount 1000000000
```

### Mass-transfer

```
lto mass-transfer <<< "3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK:1000000000 3JxcLqcAKiUyvvLS8fk9SCS4taaCKUCqqLz:800000000"
```

### Leasing

```
lto lease create --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK --amount 1000000000
lto lease cancel --leaseid 6XmeG7SRWiw8pD6Uad6D9AAaY354v5TV6AJMhPpHMkqy
```

### Sponsorship

```
lto sponsorship create --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK
lto sponsorship cancel --recipient 3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK
```

### Common options

```
--network CHAINID
--account NAME|ADDRESS
--sponsor NAME|ADDRESS
--no-broadcast
--unsigned
```
