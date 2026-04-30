# GetAvailableUnfreezeCount

查询账户剩余可发起解冻次数（Stake 2.0 一个账户最多有 32 个解冻进行中）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetAvailableUnfreezeCount (GetAvailableUnfreezeCountRequestMessage) returns (GetAvailableUnfreezeCountResponseMessage) {}
```
