# eth_newFilter

注册一个日志 filter，后续通过 [`eth_getFilterChanges`](eth_getFilterChanges.md) 拉取增量、[`eth_getFilterLogs`](eth_getFilterLogs.md) 拉取全量。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#newFilter`
- 端口：FullNode `8545` / Solidity `8555`

> **本节示例需在自有节点（如 `http://127.0.0.1:8545/jsonrpc`）测试**：filter 状态保存在单个 fullnode 进程内（`eventFilter2ResultFull` / `eventFilter2ResultSolidity`），公共网关（如 `nile.trongrid.io`）通常是反向代理到多台节点的负载均衡，连续两次请求可能落到不同节点，filter ID 在第二次请求时即视为不存在。

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | object | 是 | `FilterRequest`（字段见 [`eth_getLogs`](eth_getLogs.md)）。**不接受 `finalized`、`pending` 和 `safe` tag** |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_newFilter","params":[{"fromBlock":"latest","address":"0x4112ab345..."}],"id":1}'
```

## 响应

filter ID（`0x` 前缀的 hex 字符串）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x55b2af16ed1f4f3a..." }
```

行为：

- FullNode 端口的 filter 存于 `eventFilter2ResultFull`，Solidity 端口存于 `eventFilter2ResultSolidity`，互不可见。
- 节点出块/固化时，命中的日志会被异步追加到 filter 的 result 队列中。
- **5 分钟未被读取（`getFilterChanges` / `getFilterLogs`）即过期**（`EXPIRE_SECONDS = 300`）；过期后下一次访问抛 `-32000 filter not found`。
- 单节点同时存活的 log filter 数量受 `node.jsonrpc.maxLogFilterNum` 限制（默认 20000）。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 已存在 log filter 数量 >= `maxLogFilterNum` | `-32005` | `exceed max log filters: <N>, try again later` |
| `fromBlock` 或 `toBlock` 为 `finalized` | `-32602` | `invalid block range params` |
| `fromBlock` 或 `toBlock` 为 `pending` 或 `safe` | `-32602` | `TAG pending not supported` 或 `TAG safe not supported` |
| 其他 `FilterRequest` 校验失败 | `-32602` | 透传 `LogFilterWrapper` 校验 message |
