# GetDelegatedResourceAccountIndex

> **存量查询**：仅返回 Stake 1.0 存储的代理对手地址索引，对 V2 数据无效。源码无版本网关，可在 V2 启用后继续调用以查询历史 V1 仓位。新业务请使用 [`GetDelegatedResourceAccountIndexV2`](../stake-v2/GetDelegatedResourceAccountIndexV2.md)。

查询账户作为出借方/接收方的代理对手地址列表（Stake 1.0）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetDelegatedResourceAccountIndex (BytesMessage) returns (DelegatedResourceAccountIndex) {}
```
