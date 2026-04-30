# UnfreezeBalanceV2

发起解冻申请（Stake 2.0），进入 14 天等待期，到期后通过 `WithdrawExpireUnfreeze` 提取。

- 服务：仅支持 `Wallet`

```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```
