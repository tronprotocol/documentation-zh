# UnfreezeBalance2

> **存量保留**：与 `FreezeBalance2` 不同，本方法在 Stake 2.0 启用后**仍可正常调用**——`UnfreezeBalanceActuator` 没有 `supportUnfreezeDelay` 网关，存量 V1 仓位需要通过它解冻。新业务请使用 [`UnfreezeBalanceV2`](../stake-v2/UnfreezeBalanceV2.md)。

解冻已到期的 Stake 1.0 资产。

- 服务：仅支持 `Wallet`

```protobuf
rpc UnfreezeBalance2 (UnfreezeBalanceContract) returns (TransactionExtention) {}
```
