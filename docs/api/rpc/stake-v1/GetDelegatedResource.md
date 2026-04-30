# GetDelegatedResource

> **存量查询**：仅返回 Stake 1.0 存储的代理记录，对 V2 数据无效。源码无版本网关，可在 V2 启用后继续调用以查询历史 V1 仓位。新业务请使用 [`GetDelegatedResourceV2`](../stake-v2/GetDelegatedResourceV2.md)。

查询 from→to 之间所有的资源代理记录（Stake 1.0）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetDelegatedResource (DelegatedResourceMessage) returns (DelegatedResourceList) {}
```
