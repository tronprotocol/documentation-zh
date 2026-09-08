# 链上数据与工具

查询交易、区块和链参数，以及本地的编码工具。

## 如何获取交易信息 {#how-to-get-transaction-information}

### GetTransactionById

根据交易 ID 获取交易信息。

### GetTransactionCountByBlockNum

根据区块高度获取该区块中的交易数量。

```console
> GetTransactionCountByBlockNum number
```

### GetTransactionInfoById

根据交易 ID 获取交易信息，通常用于查看智能合约触发的结果。

### GetTransactionInfoByBlockNum

根据区块高度获取该区块中的交易信息列表。

```console
> GetTransactionInfoByBlockNum number
```

## 如何获取区块信息 {#how-to-get-block-information}

### GetBlock

根据区块号获取区块；如果不传参数，则获取最新区块。

```console
> GetBlock [BlockNum]
```

### GetBlockById

根据区块 ID 获取区块。

### GetBlockByIdOrNum

根据区块 ID 或区块高度获取区块。如果不传参数，则获取最新区块。

### GetBlockByLatestNum

```console
> GetBlockByLatestNum n
```

获取最新的 `n` 个区块，其中 0 < n < 100。

### GetBlockByLimitNext

```console
> GetBlockByLimitNext start_block_number end_block_number
```

获取区块高度区间 [start_block_number, end_block_number) 内的区块。两个参数都是区块**高度**，不是区块 id。

## 链参数与节点

### GetChainParameters

显示区块链委员会可以设置的所有参数。

```console
> GetChainParameters
```

### GetNextMaintenanceTime

获取下一个维护期的开始时间。

### ListNodes

获取其他对端节点的信息。

### BroadcastTransaction

广播以十六进制字符串表示的交易。

## 本地工具

### EncodingConverter

一个实用的编码转换器。

```console
wallet> EncodingConverter

==============================
  Encoding Converter (CLI)
==============================
1) TRON - EVM Address
2) Base64 Encode / Decode
3) Base58Check Encode / Decode
4) Public Key -> Address
5) Private Key -> Public Key & Address
0) Exit
>
```

### GetPrivateKeyByMnemonic

通过助记词获取私钥。

```console
wallet> GetPrivateKeyByMnemonic

Please enter 12 or 24 words (separated by spaces) [Attempt 1/3]:
```

## 另请参见

- [account](account.md)——账户级查询
- [vote-reward](vote-reward.md)——见证人列表
- [resources](resources.md)——资源单价
