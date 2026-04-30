# GetCanWithdrawUnfreezeAmount

查询指定时间点账户可提取的解冻金额（Stake 2.0）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetCanWithdrawUnfreezeAmount (CanWithdrawUnfreezeAmountRequestMessage) returns (CanWithdrawUnfreezeAmountResponseMessage) {}
```

相似 HTTP 接口见 [/wallet/getcanwithdrawunfreezeamount](../../http/stake-v2/getcanwithdrawunfreezeamount.md)。
