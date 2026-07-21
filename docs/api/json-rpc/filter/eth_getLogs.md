# eth_getLogs

按条件查询事件日志。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getLogs`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | object | 是 | `FilterRequest` 对象（见下） |

`FilterRequest` 字段：

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `fromBlock` | string | `latest` | 起始块；接受 `latest` / `earliest` / `finalized` 或 hex 高度（`pending` 和 `safe` 显式不支持） |
| `toBlock` | string | `latest` | 结束块；同上 |
| `address` | string \| string[] | null | 单个或多个合约地址，仅匹配该地址产生的日志 |
| `topics` | array | null | 最多 4 个 slot；每个 slot 可以是单 topic、`null`、或 topic 数组（OR 语义）；slot 间为 AND |
| `blockHash` | string | null | 若指定，等同于 `fromBlock = toBlock = 该块高`（EIP-234），与 `fromBlock` / `toBlock` 互斥 |

```bash
# 例：查询块 0x3fe1ca0 内由合约 0x9ff8fc48... 产生的所有日志
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_getLogs",
    "params":[{
      "fromBlock":"0x3fe1ca0",
      "toBlock":"0x3fe1ca0",
      "address":"0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825"
    }]
  }'
```

## 响应

`LogFilterElement` 数组（按 `address` / `topic` / 块范围匹配）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `logIndex` | hex | 日志在所属块内的全局下标 |
| `transactionIndex` | hex | 所属交易在块内下标 |
| `transactionHash` | hex | txid |
| `blockHash` | hex | 区块 hash |
| `blockNumber` | hex | 区块高度 |
| `blockTimestamp` | hex | 区块时间戳，单位秒 |
| `address` | hex | 产生日志的合约地址 |
| `data` | hex | 非 indexed 参数的 ABI 编码拼接 |
| `topics` | array | indexed 参数（首项是事件签名 hash） |
| `removed` | bool | 是否因 reorg 被回滚 |

下例为上面 curl 调用 Nile testnet 抓回的真实响应（同一条 log 也出现在该交易的 [`eth_getTransactionReceipt`](../block-and-tx-query/eth_getTransactionReceipt.md) 响应中）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "address": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
      "blockNumber": "0x3fe1ca0",
      "blockTimestamp": "0x697999ef",
      "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
      "transactionIndex": "0x0",
      "logIndex": "0x0",
      "removed": false,
      "topics": [
        "0xc66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
        "0x000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
        "0x0000000000000000000000000000000000000000000000000000000000000007"
      ],
      "data": "0x0000...05f"
    }
  ]
}
```

> log `data` 实际为 224 字节，此处仅截取首尾以节省篇幅；其它字段为节点真实返回值。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `fromBlock` / `toBlock` 是 `pending` 或 `safe` | `-32602` | `TAG pending not supported` 或 `TAG safe not supported` |
| `blockHash` 与 `fromBlock` / `toBlock` 同时给 | `-32602` | `cannot specify both BlockHash and FromBlock/ToBlock, choose one or the other` |
| `blockHash` 不匹配严格的 `(0x)?[0-9a-fA-F]{64}` hash 规则 | `-32602` | `invalid hash value` |
| `blockHash` 解码成功但节点找不到该 block | `-32602` | `invalid blockHash` |
| `fromBlock > toBlock` | `-32602` | `please verify: fromBlock <= toBlock` |
| 区间跨度超过 `maxBlockRange`（默认 5000） | `-32602` | `exceed max block range: <N>` |
| `address` 数组长度 > `maxAddressSize`（默认 1000） | `-32602` | `exceed max addresses: <N>` |
| `topics` 数组长度 > 4 | `-32602` | `topics size should be <= 4` |
| `topics` 单个 slot 是数组且元素数 > `maxSubTopics`（默认 1000） | `-32602` | `exceed max topics: <N>` |
| `topics` 元素或 `address` 不是合法 hex | `-32602` | `invalid topic(s): <值>` / `invalid address at index <i>: <值>` 等 |
| 命中数超过上限 | `-32005` | `JsonRpcTooManyResultException` 透传 message |
| 节点为 lite fullnode 且查询块已剪枝 | `-32000` | `BadItemException` / `ItemNotFoundException` 透传 message |
