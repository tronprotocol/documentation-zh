# GetRewardInfo

查询账户可领取的投票分红（未提取）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetRewardInfo (BytesMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/getReward](../../http/witness-and-governance/getReward.md)。
