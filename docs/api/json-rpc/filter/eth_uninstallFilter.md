# eth_uninstallFilter

卸载一个已注册的 filter（log filter 或 block filter）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#uninstallFilter`
- 端口：FullNode `8545` / Solidity `8555`

> **本节示例需在自有节点（如 `http://127.0.0.1:8545/jsonrpc`）测试**：filter 状态保存在单个 fullnode 进程内（`eventFilter2ResultFull` / `eventFilter2ResultSolidity`），公共网关（如 `nile.trongrid.io`）通常是反向代理到多台节点的负载均衡，连续两次请求可能落到不同节点，filter ID 在第二次请求时即视为不存在。

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | filter ID（`0x` 前缀 hex） |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_uninstallFilter","params":["0xabc123..."],"id":1}'
```

## 响应

成功时永远返回 `true`：

```json
{ "jsonrpc": "2.0", "id": 1, "result": true }
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| filter ID 不存在（已过期 / 从未注册 / 属于另一端口） | `-32000` | `filter not found` |
