# eth_newBlockFilter

注册一个块 filter，每个新块到达时把块 hash 追加到结果队列。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#newBlockFilter`
- 端口：FullNode `8545` / Solidity `8555`

> **本节示例需在自有节点（如 `http://127.0.0.1:8545/jsonrpc`）测试**：filter 状态保存在单个 fullnode 进程内（`eventFilter2ResultFull` / `eventFilter2ResultSolidity`），公共网关（如 `nile.trongrid.io`）通常是反向代理到多台节点的负载均衡，连续两次请求可能落到不同节点，filter ID 在第二次请求时即视为不存在。

## 请求参数

无（`params: []`）。

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}'
```

## 响应

filter ID（`0x` 前缀 hex）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0xabc123..." }
```

行为：

- FullNode 端口的 filter 来自最新块；Solidity 端口的 filter 来自固化块通知。
- 5 分钟未读取即过期。
- 单节点同时存活的 block filter 数量受 `node.jsonrpc.maxBlockFilterNum`（默认 50000）限制。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 已存在的 block filter 数 ≥ `maxBlockFilterNum` | `-32005` | `exceed max block filters: <N>, try again later` |
