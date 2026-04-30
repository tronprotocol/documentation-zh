# WithdrawExpireUnfreeze

提取已到期的解冻 TRX 到余额（Stake 2.0）。

- 服务：仅支持 `Wallet`

```protobuf
rpc WithdrawExpireUnfreeze (WithdrawExpireUnfreezeContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/withdrawexpireunfreeze](../../http/stake-v2/withdrawexpireunfreeze.md)。
