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

JSON-RPC 协议错误使用 `error.code` / `error.message`，业务异常映射如下（见 `TronJsonRpc.java` 注解 + `JsonRpcErrorResolver.java`）：

| 错误码 | 异常类 | 含义 |
|---|---|---|
| `-32700` | JSON parser / stream constraint exception | 请求体无法解析为 JSON（`JSON parse error`），或超过 Jackson stream constraints（透传 Jackson message） |
| `-32600` | `JsonRpcInvalidRequestException` / servlet 请求校验 | 请求体不合法、batch item 不是对象，或合约校验失败（如 `eth_call` 的 `params[1]` 既非 tag 字符串也非 `{blockNumber/blockHash}` 对象，或 `ContractValidateException`） |
| `-32601` | `JsonRpcMethodNotFoundException` | 方法不存在或当前节点类型不可用（Solidity 节点禁用 `buildTransaction`，以及一组始终不支持的方法） |
| `-32602` | `JsonRpcInvalidParamsException` | 参数不合法（hash 长度错、地址格式错、block tag 不支持等） |
| `-32603` | servlet fallback exception handler | servlet 内部错误（`Internal error`） |
| `-32000` | `JsonRpcInternalException` / `ItemNotFoundException` / `BadItemException` / `ExecutionException` / `InterruptedException` | 服务端内部错误（block 不存在、VM 执行失败、`etherbase` 未配置、filter 不存在、lite fullnode 已剪枝等） |
| `-32003` | servlet response-size guard | 响应体超过 `maxResponseSize`（`Response exceeds the limit of <N> bytes`） |
| `-32005` | `JsonRpcExceedLimitException` / `JsonRpcTooManyResultException` | 触发限额（`eth_newBlockFilter` 超过 `maxBlockFilterNum`、`eth_newFilter` 超过 `maxLogFilterNum`、请求 batch size 超过 `maxBatchSize`，或 `eth_getLogs` 日志结果超过 `LogBlockQuery.MAX_RESULT=10000`；`maxBlockRange`、`maxAddressSize`、`maxSubTopics` 等校验限额抛 `-32602`） |

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
