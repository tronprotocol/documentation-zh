# eth_getTransactionByHash

按 txid 查询交易。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionByHash`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 32 字节 txid，hex 编码 |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"],"id":1}'
```

## 响应

`TransactionResult`（见 `TransactionResult.java`）；不存在返回 `null`。

| 字段 | 类型 | 说明 |
|---|---|---|
| `hash` | hex | txid |
| `nonce` | hex | 固定 `0x` 前缀 8 字节 0（Tron 无账户 nonce） |
| `blockHash` | hex | 所在区块 hash；**未上链**或调用方为待确认交易时返回 `0x` |
| `blockNumber` | hex | 同上，未上链时 `0x` |
| `transactionIndex` | hex | 块内交易下标；未上链时 `0x` |
| `from` | hex | 发起地址 |
| `to` | hex \| null | 目标地址；合约创建时为 `null` |
| `gas` | hex | 交易 energy 实际用量（**非** `feeLimit`） |
| `gasPrice` | hex | 出块时刻的 energy 单价 |
| `value` | hex | 转账金额（sun，TRX 转账有值；其他合约可能为 0） |
| `input` | hex | 调用数据（智能合约 trigger 时为 selector+args；其他合约类型为 `0x`） |
| `type` | hex | 固定 `0x0`（legacy 类型） |
| `v` / `r` / `s` | hex | 签名分量（首签）；未签名时全 0 |

下例为上面 curl 调用 Nile testnet 抓回的真实响应（合约调用类型，交易在块 `0x3fe1ca0` 内 index `0x0`，可在 [Nile Tronscan](https://nile.tronscan.org/#/transaction/01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca) 反查）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "hash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
    "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "blockNumber": "0x3fe1ca0",
    "transactionIndex": "0x0",
    "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
    "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
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
}
```

> `input` 实际长度 580 字节（合约 selector `0xa6bd98ac` + 参数），此处仅截取首尾以节省篇幅；其它字段为节点真实返回值。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 不匹配 `(0x)?[0-9a-fA-F]{64}` | `-32602` | `invalid hash value` |
