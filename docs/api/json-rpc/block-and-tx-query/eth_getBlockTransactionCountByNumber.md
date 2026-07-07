# eth_getBlockTransactionCountByNumber

按高度或 tag 查询区块内交易数。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockTransactionCountByNumber`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 区块高度（hex）或 tag（`latest` / `earliest` / `finalized`；`pending` 和 `safe` 显式不支持） |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockTransactionCountByNumber","params":["0x3fe1ca0"],"id":1}'
```

## 响应

交易数的 hex 编码。块不存在时返回 `null`。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（块 `0x3fe1ca0` 共 4 笔交易）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x4" }
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 是 `pending` 或 `safe` | `-32602` | `TAG pending not supported` 或 `TAG safe not supported` |
| `params[0]` 不是合法 hex 也不是合法 tag | `-32602` | `invalid block number` |
