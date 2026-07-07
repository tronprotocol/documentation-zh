# eth_getTransactionReceipt

按 txid 查询交易回执。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionReceipt`
- 数据结构：`framework/src/main/java/org/tron/core/services/jsonrpc/types/TransactionReceipt.java`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 32 字节 txid |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"],"id":1}'
```

## 响应

`TransactionReceipt` 对象，未找到（如交易尚未生成 `TransactionInfo`）返回 `null`。

| 字段 | 类型 | 说明 |
|---|---|---|
| `blockHash` / `blockNumber` / `transactionIndex` | hex | 所在块定位信息 |
| `transactionHash` | hex | txid |
| `from` / `to` | hex | 地址 |
| `cumulativeGasUsed` | hex | 块内累计至本交易（含本交易）的 energy 总用量 |
| `gasUsed` | hex | 本交易 energy 用量 |
| `effectiveGasPrice` | hex | 出块时刻 energy 单价（sun） |
| `contractAddress` | hex | 仅 `CreateSmartContract` 类型有值 |
| `logs` | array | 日志数组（包含 `logIndex`、`address`、`data`、`topics[]`、`blockHash`、`blockNumber`、`blockTimestamp`、`transactionHash`、`transactionIndex`、`removed`） |
| `logsBloom` | hex | 固定 256 字节 0 |
| `status` | hex | `0x1` 成功 / `0x0` 失败（基于 `TransactionInfo.resultValue <= 1`） |
| `type` | hex | 固定 `0x0` |
| `root` | null | 不填充（post-Byzantium） |

> **注意**：解析上方 `logs` 之前，请先确认交易 `status` 为 `"0x1"`——这是保证数据一致性的推荐做法。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（合约调用产生 1 条 log，可在 [Nile Tronscan](https://nile.tronscan.org/#/transaction/01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca) 反查）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "blockNumber": "0x3fe1ca0",
    "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
    "transactionIndex": "0x0",
    "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
    "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
    "cumulativeGasUsed": "0xae29",
    "gasUsed": "0xae29",
    "effectiveGasPrice": "0x64",
    "contractAddress": null,
    "logs": [
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
    ],
    "logsBloom": "0x0000...0000",
    "status": "0x1",
    "type": "0x0"
  }
}
```

> log `data` 实际为 224 字节，此处仅截取首尾以节省篇幅；`logsBloom` 实际为 256 字节全 0；其它字段为节点真实返回值。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 不匹配 `(0x)?[a-zA-Z0-9]{64}` | `-32602` | `invalid hash value` |
| `params[0]` 是合法 64 字符但解码失败 | `-32602` | 透传 `ByteArray.fromHexString` 异常 message |
