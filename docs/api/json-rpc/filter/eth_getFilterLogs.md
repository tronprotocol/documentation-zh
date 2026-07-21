# eth_getFilterLogs

按 filter 当前的 `[fromBlock, toBlock]` 重新执行一次 `eth_getLogs` 等价查询，返回**全量**结果（**不**消费队列、**不**重置过期计时；语义上等价于把 filter 当作 saved query 执行）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getFilterLogs`
- 端口：FullNode `8545` / Solidity `8555`

> **本节示例需在自有节点（如 `http://127.0.0.1:8545/jsonrpc`）测试**：filter 状态保存在单个 fullnode 进程内（`eventFilter2ResultFull` / `eventFilter2ResultSolidity`），公共网关（如 `nile.trongrid.io`）通常是反向代理到多台节点的负载均衡，连续两次请求可能落到不同节点，filter ID 在第二次请求时即视为不存在。

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | log filter ID（由 `eth_newFilter` 返回；不接受 block filter ID） |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getFilterLogs","params":["0xabc123..."],"id":1}'
```

## 响应

`LogFilterElement` 数组（字段见 [`eth_getLogs`](eth_getLogs.md)）。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| filter ID 不存在 / 已过期 / 属于 block filter 或另一端口 | `-32000` | `filter not found` |
| 已保存 filter 范围超过 `maxBlockRange`（默认 5000） | `-32602` | `exceed max block range: <N>` |
| 命中数超过上限 | `-32005` | `JsonRpcTooManyResultException` 透传 message |
| 节点为 lite fullnode 且查询块已剪枝 | `-32000` | `BadItemException` / `ItemNotFoundException` 透传 message |
