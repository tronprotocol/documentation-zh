# GetAccountBalance

按指定区块查询账户的 TRX 余额（带 block 锚点）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetAccountBalance (AccountBalanceRequest) returns (AccountBalanceResponse) {}
```

相似 HTTP 接口见 [/wallet/getaccountbalance](../../http/account/getaccountbalance.md)。
