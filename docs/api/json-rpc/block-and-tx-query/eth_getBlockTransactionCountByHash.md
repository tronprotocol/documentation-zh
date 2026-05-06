# eth_getBlockTransactionCountByHash

按 hash 查询区块内交易数。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockTransactionCountByHash`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 32 字节区块 hash |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockTransactionCountByHash","params":["0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c"],"id":1}'
```

## 响应

`block.getTransactionsList().size()` 的 hex 编码。块不存在时返回 `null`。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（块 `0x3fe1ca0` 共 4 笔交易）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x4" }
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 不匹配 `(0x)?[a-zA-Z0-9]{64}` | `-32602` | `invalid hash value` |
| `params[0]` 是合法 64 字符但解码失败 | `-32602` | 透传 `ByteArray.fromHexString` 异常 message |
