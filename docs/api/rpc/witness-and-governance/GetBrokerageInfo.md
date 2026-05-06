# GetBrokerageInfo

查询 SR 当前周期的分红比例（佣金）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetBrokerageInfo (BytesMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/getBrokerage](../../http/witness-and-governance/getBrokerage.md)。
