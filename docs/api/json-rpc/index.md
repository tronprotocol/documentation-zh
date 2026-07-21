# java-tron JSON-RPC API 文档

本目录收录 `framework/src/main/java/org/tron/core/services/jsonrpc/` 下 JSON-RPC 接口的请求/响应文档。每个方法一个 markdown 文件，命名同 `method` 字段（例如 `eth_blockNumber` → `eth_blockNumber.md`）。

## 服务与默认端口

| 服务 | 默认端口 | 启用开关 | 数据来源 |
|---|---|---|---|
| FullNode JSON-RPC | `8545` | `node.jsonrpc.httpFullNodeEnable` | 全量数据库（最新块即可见） |
| Solidity JSON-RPC | `8555` | `node.jsonrpc.httpSolidityEnable` | 仅固化数据 |

端口可通过 `node.jsonrpc.httpFullNodePort` / `httpSolidityPort` 覆盖（参见 `framework/src/main/resources/config.conf` 的 `jsonrpc {}` 段）。

> **默认关闭**：`config.conf` 中 `jsonrpc {}` 块的所有开关默认注释掉，`Args` 中 `httpFullNodeEnable` / `httpSolidityEnable` 均为 `false`（见 `Args.java`）。需在配置中显式 `httpFullNodeEnable = true` / `httpSolidityEnable = true` 才会随节点启动。Solidity JSON-RPC 服务还要求当前进程为 FullNode（不是独立的 SolidityNode 进程，见 `JsonRpcServiceOnSolidity.java`）。

URL 路径恒为 `/jsonrpc`（见 `FullNodeJsonRpcHttpService.java`）。

## 协议约定

- **传输**：仅 `POST`，请求体为 [JSON-RPC 2.0](https://www.jsonrpc.org/specification) 格式：`{"jsonrpc":"2.0","method":"...","params":[...],"id":1}`。
- **HTTP 状态码**：请求进入 `JsonRpcServlet` 后，JSON-RPC 业务错误以 HTTP 200 加响应体 `error` 字段返回。传输层失败仍可能返回非 200 状态码，例如请求体过大可能在 servlet 分发前被拒绝。
- **数值编码**：响应中的 quantity 使用 `0x` 前缀十六进制字符串。区块查询 selector 还接受非负十进制高度，因为 `JsonRpcApiUtil.parseBlockNumber` 同时支持十进制和 `0x` 前缀输入。
- **地址编码**：JSON-RPC 的状态查询、调用和交易构造接口只接受十六进制地址：20 字节 EVM 风格地址，或以 `41` 开头的 21 字节 Tron 地址；均可带或不带 `0x`。`JsonRpcApiUtil.addressCompatibleToByteArray` 不接受 base58check（`T...`）。日志过滤器使用 20 字节十六进制地址。
- **调用数据字段**：`eth_call`、`eth_estimateGas` 和 `buildTransaction` 同时接受 `data` 与 `input`。`input` 使用更严格的 execution API hex 规则（必须带 `0x` 前缀、长度为偶数；空字符串表示空 bytes）。`data` 为兼容旧客户端保留较宽松解析。
- **block tag**：常见的 `latest` / `earliest` / `pending` / `finalized` / `safe` 中，**只有少量方法支持**：
    - `eth_getBlockByNumber`、`eth_getBlockReceipts` 等区块查询方法接受 `latest` / `earliest` / `finalized`；`pending` 和 `safe` 显式不支持，会抛 `-32602 TAG pending not supported` 或 `-32602 TAG safe not supported`。
    - `eth_getBalance` / `eth_getStorageAt` / `eth_getCode` / `eth_call` **只支持 `latest`**，传 `earliest` / `pending` / `finalized` / `safe` 抛 `-32602 TAG [earliest | pending | finalized | safe] not supported`，传具体高度抛 `-32602 QUANTITY not supported, just support TAG as latest`。
    - `eth_newFilter` 不支持 `finalized`（抛 `-32602 invalid block range params`），也不支持 `pending` 和 `safe`（抛对应的 `TAG ... not supported`）。

## 异常响应

<!-- BEGIN GENERATED JSON-RPC ERROR CATALOG -->
### JSON-RPC 错误目录

Catalog ID 和重试分类由 `openrpc.json` 的 `x-tron-error-model` 定义。它们是机器可读的文档分类，不是 java-tron 在线上响应中返回的字段。

`自动重试` 与 catalog 的 `retryable` 完全对应：只有“是”才允许自动重放同一逻辑操作。有条件的重试类别在满足“范围 / 操作”的前置条件之前仍为“否”。

先评估 `sharedCatalogIds` 引用的可执行匹配，再通过 method 的 `x-tron-error-catalog` 限定 method 声明的候选错误。`sourceException` 是源码元数据，不是线上字段。如果 `-32000` 或 `-32005` 等重用错误码仍对应多个候选项，则将响应分类为 `UNKNOWN`，且不得自动重试。

| Catalog ID | 线上信号 | 源码声明 | 含义 | 自动重试 | 重试类别 | 范围 / 操作 |
|---|---|---|---|---|---|---|
| `JSON_RPC_PARSE_ERROR` | `error.code` = `-32700` | — | 请求体不是有效 JSON。 | 否 | `AFTER_REQUEST_REBUILD` | 修正 JSON 语法，或减少超过 parser 限制的结构后重新提交。 |
| `JSON_RPC_INVALID_REQUEST` | `error.code` = `-32600` | `JsonRpcInvalidRequestException` | JSON 值不是有效的 JSON-RPC 2.0 请求。 | 否 | `AFTER_REQUEST_REBUILD` | 修正 JSON-RPC envelope 或无效 batch item 后重新提交。 |
| `JSON_RPC_METHOD_NOT_FOUND` | `error.code` = `-32601` | `JsonRpcMethodNotFoundException` | 当前节点/port 不可用或不支持请求的 method。 | 否 | `AFTER_STATE_CHANGE` | 使用兼容节点/port，或等待节点可用性或配置变更。 |
| `JSON_RPC_INVALID_PARAMS` | `error.code` = `-32602` | `JsonRpcInvalidParamsException` | 一个或多个 method 参数无效。 | 否 | `AFTER_REQUEST_REBUILD` | 修正参数数量、类型、格式、block tag 或范围后重新提交。 |
| `JSON_RPC_SERVLET_INTERNAL_ERROR` | `error.code` = `-32603` 且 `error.message` = `Internal error` | — | JSON-RPC servlet 捕获到未预期的兜底异常。 | 否 | `UNKNOWN` | 检查节点日志或使用其它健康节点；不得仅根据该兜底分类自动重试。 |
| `JSON_RPC_RESPONSE_TOO_LARGE` | `error.code` = `-32003` 且 `error.message` 以 `Response exceeds the limit of ` 开头 | — | 编码后的 JSON-RPC 响应超过 `maxResponseSize`。 | 否 | `AFTER_REQUEST_REBUILD` | 缩小或拆分查询，使编码后的响应不超过 `maxResponseSize`。 |
| `JSON_RPC_BATCH_TOO_LARGE` | `error.code` = `-32005` 且 `error.message` 以 `Batch size ` 开头 | — | 请求 batch 条目数超过 `maxBatchSize` 限制。 | 否 | `AFTER_REQUEST_REBUILD` | 拆分 batch，确保每个请求的条目数不超过 `maxBatchSize`。 |
| `JSON_RPC_FILTER_LIMIT_EXCEEDED` | `error.code` = `-32005` | `JsonRpcExceedLimitException` | 节点已达活跃 filter 数量上限。 | 否 | `AFTER_STATE_CHANGE` | 仅在 filter 容量释放后重试，或使用其它节点。 |
| `JSON_RPC_TOO_MANY_RESULTS` | `error.code` = `-32005` | `JsonRpcTooManyResultException` | 日志查询返回的结果数将超过节点限制。 | 否 | `AFTER_REQUEST_REBUILD` | 缩小 block 范围、address 或 topic 后重新提交。 |
| `JSON_RPC_UNDERLYING_INTERNAL_ERROR` | `error.code` = `-32001` 加 fallback 匹配 | `JsonRpcInternalException`；message 元数据 `<underlying exception message>` | 链标识查询失败，并返回底层异常消息。 | 否 | `UNKNOWN` | 检查返回消息和节点上下文；如无具体瞬时原因，不得自动重试。 |
| `JSON_RPC_INTERNAL_ERROR` | `error.code` = `-32000` | `JsonRpcInternalException` | method 引发了 java-tron JSON-RPC 内部错误。 | 否 | `UNKNOWN` | 检查 `error.message` 和节点日志；如无更具体的分类，不得自动重试。 |
| `JSON_RPC_ITEM_NOT_FOUND` | `error.code` = `-32000` | `ItemNotFoundException` | 请求的 filter、block item 或缓存项不存在。 | 否 | `AFTER_STATE_CHANGE` | 重新创建缺失的 filter，等待 item 可用，或使用具有请求数据的节点。 |
| `JSON_RPC_BAD_ITEM` | `error.code` = `-32000` | `BadItemException` | 日志处理遇到无效底层 item。 | 否 | `UNKNOWN` | 检查无效底层 item 和查询上下文；不得自动重试。 |
| `JSON_RPC_EXECUTION_ERROR` | `error.code` = `-32000` | `ExecutionException` | 异步日志查询执行失败。 | 否 | `UNKNOWN` | 检查异步执行失败和节点日志，再决定是否再次尝试。 |
| `JSON_RPC_INTERRUPTED` | `error.code` = `-32000` | `InterruptedException` | 日志查询执行声明了 InterruptedException，但线上响应无法将其与其它 `-32000` 失败安全区分。 | 否 | `UNKNOWN` | 当前线上响应与其它 `-32000` 失败存在歧义；不得自动重试。 |
| `JSON_RPC_RATE_LIMITED` | JSON-RPC envelope 之外的 HTTP 200，且 `$.Error` 包含 `lack of computing resources` | — | 共享 servlet 限流器在写入 JSON-RPC envelope 前拒绝了请求。 | 是 | `SAFE_WITH_BACKOFF` | 使用带抖动的指数退避自动重试；响应不包含 Retry-After header。 |
| `JSON_RPC_REQUEST_TOO_LARGE` | JSON-RPC envelope 之外的 HTTP 413 | — | HTTP 请求体在 servlet dispatch 前超过 `node.jsonrpc.maxMessageSize`。 | 否 | `AFTER_REQUEST_REBUILD` | 缩小 HTTP 请求体后重新提交。 |
<!-- END GENERATED JSON-RPC ERROR CATALOG -->

错误响应示例：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "invalid hash value",
    "data": "{}"
  }
}
```

> **注意**：`disabledApi` 配置项**不影响 JSON-RPC**（见 `config.conf` 注释 "but not jsonrpc"）。要禁用 JSON-RPC，请关闭对应 `httpFullNodeEnable` / `httpSolidityEnable`。

## 节点信息 / 链身份

| 方法 | 说明 |
|---|---|
| [`web3_clientVersion`](node/web3_clientVersion.md) | 客户端版本字符串 |
| [`web3_sha3`](node/web3_sha3.md) | Keccak-256 hash |
| [`net_version`](node/net_version.md) | 网络 ID（同 `eth_chainId`） |
| [`net_listening`](node/net_listening.md) | 是否在监听 P2P |
| [`net_peerCount`](node/net_peerCount.md) | 对等节点数 |
| [`eth_chainId`](node/eth_chainId.md) | chainId（创世块 hash 后 4 字节） |
| [`eth_protocolVersion`](node/eth_protocolVersion.md) | 当前块 header 的协议版本号 |
| [`eth_syncing`](node/eth_syncing.md) | 同步状态 |
| [`eth_blockNumber`](node/eth_blockNumber.md) | 最新块高 |
| [`eth_gasPrice`](node/eth_gasPrice.md) | 当前 energy 单价（sun） |

## 区块 / 交易查询

| 方法 | 说明 |
|---|---|
| [`eth_getBlockByHash`](block-and-tx-query/eth_getBlockByHash.md) | 按 hash 查询块 |
| [`eth_getBlockByNumber`](block-and-tx-query/eth_getBlockByNumber.md) | 按高度/tag 查询块 |
| [`eth_getBlockTransactionCountByHash`](block-and-tx-query/eth_getBlockTransactionCountByHash.md) | 块内交易数（按 hash） |
| [`eth_getBlockTransactionCountByNumber`](block-and-tx-query/eth_getBlockTransactionCountByNumber.md) | 块内交易数（按高度） |
| [`eth_getTransactionByHash`](block-and-tx-query/eth_getTransactionByHash.md) | 按 txid 查询交易 |
| [`eth_getTransactionByBlockHashAndIndex`](block-and-tx-query/eth_getTransactionByBlockHashAndIndex.md) | 按块 hash + index 查询交易 |
| [`eth_getTransactionByBlockNumberAndIndex`](block-and-tx-query/eth_getTransactionByBlockNumberAndIndex.md) | 按块高 + index 查询交易 |
| [`eth_getTransactionReceipt`](block-and-tx-query/eth_getTransactionReceipt.md) | 按 txid 查询回执 |
| [`eth_getBlockReceipts`](block-and-tx-query/eth_getBlockReceipts.md) | 整块回执列表 |

## 账户状态

| 方法 | 说明 |
|---|---|
| [`eth_getBalance`](account/eth_getBalance.md) | 账户 TRX 余额（sun） |
| [`eth_getStorageAt`](account/eth_getStorageAt.md) | 合约存储槽 |
| [`eth_getCode`](account/eth_getCode.md) | 合约 runtime 字节码 |

## 智能合约调用

| 方法 | 说明 |
|---|---|
| [`eth_call`](smart-contract/eth_call.md) | 只读调用合约 |
| [`eth_estimateGas`](smart-contract/eth_estimateGas.md) | 估算 energy 消耗 |

## 日志 / 过滤器

| 方法 | 说明 |
|---|---|
| [`eth_getLogs`](filter/eth_getLogs.md) | 一次性日志查询 |
| [`eth_newFilter`](filter/eth_newFilter.md) | 注册日志 filter |
| [`eth_newBlockFilter`](filter/eth_newBlockFilter.md) | 注册新块 filter |
| [`eth_uninstallFilter`](filter/eth_uninstallFilter.md) | 卸载 filter |
| [`eth_getFilterChanges`](filter/eth_getFilterChanges.md) | 拉取并清空 filter 增量 |
| [`eth_getFilterLogs`](filter/eth_getFilterLogs.md) | 拉取 log filter 全量（不清空） |

filter 相关默认限额（见 `config.conf` 的 `jsonrpc {}` 段）：

| 配置项 | 默认值 | 含义 |
|---|---|---|
| `maxBlockRange` | 5000 | `eth_getLogs` 与 `eth_getFilterLogs` 单次允许的 `[fromBlock, toBlock]` 跨度 |
| `maxAddressSize` | 1000 | 单次 filter 请求允许的地址数量 |
| `maxSubTopics` | 1000 | 单个 topic slot 允许的 OR 候选数 |
| `maxBlockFilterNum` | 50000 | 单节点同时存活的 block filter 上限 |
| `maxLogFilterNum` | 20000 | 单节点同时存活的 log filter 上限 |
| `maxBatchSize` | 100 | JSON-RPC batch 请求最大条数 |
| `maxResponseSize` | 26214400 | 响应体大小上限，单位 bytes（25 MiB） |
| `maxMessageSize` | 4194304 | JSON-RPC 请求体大小上限，单位 bytes（约 4 MiB）；独立于 HTTP/gRPC 限制 |

## 交易构造

| 方法 | 说明 |
|---|---|
| [`buildTransaction`](tx-build/buildTransaction.md) | 构造未签名交易（仅 FullNode；TRX 转账 / TRC-10 转账 / 部署合约 / 触发合约） |

> JSON-RPC 不提供广播接口；签名后请走 HTTP [`/wallet/broadcasttransaction`](../http/tx-build-and-broadcast/broadcasttransaction.md) 或 [`/wallet/broadcasthex`](../http/tx-build-and-broadcast/broadcasthex.md)。

## 兼容桩方法

Tron 是 DPoS 共识，没有 PoW 工作量、uncle、矿工概念，下列方法仅为兼容标准 ETH 客户端而保留，永远返回常量：

| 方法 | 返回 | 说明 |
|---|---|---|
| [`eth_coinbase`](stub/eth_coinbase.md) | 配置的 etherbase 地址 | 未配置时抛 `-32000 etherbase must be explicitly specified` |
| [`eth_accounts`](stub/eth_accounts.md) | `[]` | 节点不托管私钥 |
| [`eth_getWork`](stub/eth_getWork.md) | `[blockHash, null, null]` | 当前块 hash + 两个 null |
