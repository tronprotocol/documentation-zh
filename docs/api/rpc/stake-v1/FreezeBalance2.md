# FreezeBalance2

> **链上已禁用**：提案 #70 `UNFREEZE_DELAY_DAYS` 通过后（主网已生效），`FreezeBalanceActuator.validate()` 会直接抛出 `freeze v2 is open, old freeze is closed`，新请求一律失败。请改用 [`FreezeBalanceV2`](../stake-v2/FreezeBalanceV2.md)。
>
> 注：方法名末尾的 `2` 是 proto 历史命名后缀（返回 `TransactionExtention`），与 Stake 2.0 的 `FreezeBalanceV2` 不是同一个方法。

冻结 TRX 获取带宽或能量，可代理给他人。冻结期最少 3 天。

- 服务：仅支持 `Wallet`

```protobuf
rpc FreezeBalance2 (FreezeBalanceContract) returns (TransactionExtention) {}
```
