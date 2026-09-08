# eth_getBlockByHash

按区块 hash 查询区块。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockByHash`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 32 字节区块 hash，hex 编码（带或不带 `0x`） |
| `params[1]` | bool | 是 | `true` 返回完整 `TransactionResult` 对象数组；`false` 仅返回 txid 数组 |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params":["0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c", true],"id":1}'
```

## 响应

返回 `BlockResult` 对象（见 `BlockResult.java`），未找到时返回 `null`。字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `number` | hex | 区块高度 |
| `hash` | hex | 区块 hash（即 BlockId，前 8 字节为高度大端编码） |
| `parentHash` | hex | 父块 hash |
| `nonce` | hex | 固定 8 字节 0（Tron 无 PoW） |
| `sha3Uncles` | hex | 固定 32 字节 0（Tron 无叔块） |
| `logsBloom` | hex | 固定 256 字节 0（块级 bloom 不维护） |
| `transactionsRoot` | hex | 交易 trie root |
| `stateRoot` | hex | 账户状态 root |
| `receiptsRoot` | hex | 固定 32 字节 0 |
| `miner` | hex | 出块超级代表地址（创世块为全 0） |
| `difficulty` / `totalDifficulty` | hex | 固定 `0x0` |
| `extraData` | hex | 固定 `0x` |
| `size` | hex | 序列化字节数 |
| `gasLimit` | hex | 块内所有交易 `feeLimit` 之和 |
| `gasUsed` | hex | 块内所有交易 energy 用量之和 |
| `timestamp` | hex | 区块时间戳，**秒**（proto 里是毫秒，此处除以 1000） |
| `transactions` | array | `params[1]=true` 时为 `TransactionResult` 对象数组；否则为 `0x` 前缀 txid 字符串数组 |
| `uncles` | array | 固定空数组 `[]` |
| `baseFeePerGas` | hex | 固定 `0x0`（不收 EIP-1559 base fee） |
| `mixHash` | hex | 固定 32 字节 0 |

下例为上面 curl 调用 Nile testnet 抓回的真实响应（块高 `0x3fe1ca0` = 67026080，可在 [Nile Tronscan](https://nile.tronscan.org/#/block/67026080) 反查）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "number": "0x3fe1ca0",
    "hash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "parentHash": "0x0000000003fe1c9f1030bf08074186a7c119391405507ce6cceb95855f5ef164",
    "miner": "0xa234e405a2c6fd67cdd4d0ea2f6188f65534c8b1",
    "timestamp": "0x69f18c42",
    "size": "0x60a",
    "transactionsRoot": "0xb488e770d80b4431e356111db97fca5b14f3f6a4d630c565ff15ee4ed9abee72",
    "stateRoot": "0x",
    "transactions": [
      {
        "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
        "blockNumber": "0x3fe1ca0",
        "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
        "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
        "hash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
        "transactionIndex": "0x0",
        "value": "0x0",
        "gas": "0xae29",
        "gasPrice": "0x64",
        "input": "0xa6bd98ac0000...0000",
        "type": "0x0",
        "nonce": "0x0000000000000000",
        "v": "0x1b",
        "r": "0x2154e8ef08f014063de8a88bafe748c8cbb48633c1657c083dca1a73439b289f",
        "s": "0x6aa796bfa58797da6354d35fb7334a8c145c48ae266e4a885f7ee44791b5a3c3"
      }
    ],
    "uncles": [],
    "gasLimit": "0x2540be400",
    "gasUsed": "0xae29",
    "difficulty": "0x0",
    "totalDifficulty": "0x0",
    "extraData": "0x",
    "logsBloom": "0x0000...0000",
    "nonce": "0x0000000000000000",
    "sha3Uncles": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "receiptsRoot": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "baseFeePerGas": "0x0"
  }
}
```

> 该块共 4 笔交易，仅展示首笔合约调用（`transactionIndex: 0x0`）。`input` 实际长度 580 字节（合约 selector `0xa6bd98ac` + 参数），此处仅截取首尾以节省篇幅。`logsBloom` 实际为 256 字节全 0；其它字段为节点真实返回值。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 不匹配 `(0x)?[0-9a-fA-F]{64}` | `-32602` | `invalid hash value` |
