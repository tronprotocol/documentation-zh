# java-tron API 接口

java-tron 节点对外暴露三套 API。它们底层能力大体一致，区别在于传输方式、编码格式以及生态适配。请优先按照客户端环境选择，仅当某个方法只有特定 API 才支持时再以"功能覆盖"为依据。

## 如何选择

| 需求 | 推荐方案 | 原因 |
|---|---|---|
| 在浏览器、移动端或任意 HTTP 客户端中调用 | **HTTP 接口** | `POST` / `GET`（部分支持），无需代码生成，节点上方法覆盖最广 |
| 复用以太坊生态工具（web3.js、ethers.js、MetaMask、Hardhat、Foundry 等） | **JSON-RPC 接口** | 实现了 `eth_*` / `net_*` / `web3_*` 方法集，EVM 工具可直接使用 |
| 用强类型语言（Java、Go、Rust、C++）做服务端对接，且对延迟或吞吐有要求 | **gRPC 接口** | 基于 HTTP/2 长连接，protobuf 编码，自动生成 stub |

如果暂时无法决定：先从 **HTTP 接口** 入手。它部署成本最低，方法覆盖最广。仅当目标是兼容 EVM 工具时改用 JSON-RPC；只有在性能分析显示 HTTP 通路是瓶颈时才切换到 gRPC。

注意事项：

- 三套 API 连接的是同一份底层数据库。选哪一套并不会限制可读取的数据，只会限制可用的方法名和数据结构。
- 每套 API 的 Solidity 后缀变体仅返回固化数据（即已超过不可逆阈值的区块）。需要终局性时使用，代价是约 1 分钟的滞后。

## 参考索引

- [HTTP 接口参考](http/index.md) —— `/wallet/*` 与 `/walletsolidity/*`（部分支持）下的端点，按功能模块组织
- [JSON-RPC 接口参考](json-rpc/index.md) —— `eth_*` / `net_*` / `web3_*` 方法以及 Tron 专属的 `buildTransaction`
- [gRPC 接口参考](rpc/index.md) —— `protocol.Wallet` / `protocol.WalletSolidity`（部分支持）方法
