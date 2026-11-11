# UnfreezeBalanceV2

发起解冻申请（Stake 2.0）。等待期由链参数 `UNFREEZE_DELAY_DAYS` 决定（当前主网值为 14 天），到期后可通过 `WithdrawExpireUnfreeze` 提取。

- 服务：仅支持 `Wallet`

```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/unfreezebalancev2](../../http/stake-v2/unfreezebalancev2.md)。
