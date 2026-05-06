# eth_getFilterChanges

拉取 filter 自上次读取以来的增量结果，**并清空队列、重置过期计时**。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getFilterChanges`
- 端口：FullNode `8545` / Solidity `8555`

> **本节示例需在自有节点（如 `http://127.0.0.1:8545/jsonrpc`）测试**：filter 状态保存在单个 fullnode 进程内（`eventFilter2ResultFull` / `eventFilter2ResultSolidity`），公共网关（如 `nile.trongrid.io`）通常是反向代理到多台节点的负载均衡，连续两次请求可能落到不同节点，filter ID 在第二次请求时即视为不存在。

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | filter ID（`0x` 前缀 hex），由 `eth_newFilter` 或 `eth_newBlockFilter` 返回 |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":["0xabc123..."],"id":1}'
```

## 响应

返回类型取决于 filter 种类：

- block filter → 块 hash 字符串数组（`0x` 前缀 32 字节 hex）
- log filter → `LogFilterElement` 数组（字段同 [`eth_getLogs`](eth_getLogs.md)）

调用后队列被清空，过期计时重新计为 5 分钟。

```json
{ "jsonrpc": "2.0", "id": 1, "result": [
  "0x000000000048d3198a657ce15a8c80b66db8de58e3df9d5612eb1d80a98e4cee",
  "0x000000000048d31a..."
]}
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| filter ID 不存在 / 已过期 / 属于另一端口 | `-32000` | `filter not found` |
