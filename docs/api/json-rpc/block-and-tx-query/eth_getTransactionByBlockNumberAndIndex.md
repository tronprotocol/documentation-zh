# eth_getTransactionByBlockNumberAndIndex

按区块高度 + 块内 index 查询交易。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionByBlockNumberAndIndex`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 区块高度（hex）或 tag（`latest` / `earliest` / `finalized`；`pending` 和 `safe` 显式不支持） |
| `params[1]` | string | 是 | 块内交易下标，hex 编码 |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionByBlockNumberAndIndex","params":["0x3fe1ca0","0x0"],"id":1}'
```

## 响应

`TransactionResult`（字段见 [`eth_getTransactionByHash`](eth_getTransactionByHash.md)）；块不存在或 index 越界返回 `null`。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（同 [`eth_getTransactionByHash`](eth_getTransactionByHash.md) 中展示的合约调用交易）：

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

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 是 `pending` 或 `safe` | `-32602` | `TAG pending not supported` 或 `TAG safe not supported` |
| `params[0]` 不是合法 hex 也不是合法 tag | `-32602` | `invalid block number` |
| `params[1]` 不是合法 hex | `-32602` | `invalid index value` |
