# wallet-cli block

获取区块（省略参数时取最新区块）。

## 用法

```
wallet-cli block [<number>] [options]
```

## 参数

- `number`——要获取的区块高度；省略则取最新区块

## 选项

仅[全局选项](index.md)。

## 注意事项

需要 `--network`（或 config.defaultNetwork）。TRON 与 EVM 网络均可使用；区块号是所选链自己的高度。

## 示例

```bash
wallet-cli block --network tron:3448148188
```

```console
Number        #70,433,745
Time          2026-08-27 08:17:54 UTC
Transactions  5
```

```bash
wallet-cli block 70433745 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"block","data":{"block":{"blockID":"0000000041e6a3c3…","block_header":{"raw_data":{"number":70433745,"txTrieRoot":"…","witness_address":"41…","parentHash":"…","version":31,"timestamp":1787818674000},"witness_signature":"…"},"transactions":[{}]}},"meta":{"durationMs":126,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 网络上，文本摘要给出的是该链区块真正拥有的 gas 与费用数据：

```bash
wallet-cli block --network eip155:11155111
```

```console
Number        #11,576,585
Hash          0xfbebc32aba432b2ae721b062cf40d2cb685f1ba617f0f5d3fc8e768b53a8d820
Parent hash   0x222ceb99e43496964a36be6ee98137f4ca51d4e2d88a25c56bf48007d57ec0bd
Time          2026-08-27 08:06:24 UTC
Transactions  197
Gas used      18,543,035 / 60,000,000
Base fee      1.119025 gwei
```

## 输出

`data.block` 是节点返回的原始区块，未经任何修改——在 TRON 上是 TRON 区块对象，在 EVM 上是 `eth_getBlockByNumber` 的结果。其确切结构与节点的区块结构一致，因此**只有文本摘要是跨家族归一化的**；关键字段见下表（上面示例中较长的哈希和完整交易列表以 `…` 省略）。

TRON：

| 字段 | 类型 | 含义 |
|---|---|---|
| `block.blockID` | string | 区块哈希 |
| `block.block_header.raw_data.number` | number | 区块高度 |
| `block.block_header.raw_data.timestamp` | number | 出块时间（epoch 以来的毫秒数，UTC） |
| `block.block_header.raw_data.witness_address` | string | 出块的 SR，hex 格式（`41…`） |
| `block.transactions` | array | 区块内的交易（为空时省略该字段） |

EVM——全部沿用节点自身的十六进制 QUANTITY 编码：

| 字段 | 类型 | 含义 |
|---|---|---|
| `block.hash` / `block.parentHash` | string | 区块哈希与父区块哈希 |
| `block.number` | string | 区块高度，十六进制（`"0xb0a509"`） |
| `block.timestamp` | string | 出块时间，十六进制，epoch 以来的秒数 |
| `block.gasUsed` / `block.gasLimit` | string | 已消耗与已授权的 gas，十六进制 |
| `block.baseFeePerGas` | string | 每单位 gas 的基础费用，十六进制 wei |
| `block.miner` | string | 该区块归属的地址 |
| `block.transactions` | array | 交易哈希，或节点返回的完整交易对象 |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[网络](../concepts/networks.md)
