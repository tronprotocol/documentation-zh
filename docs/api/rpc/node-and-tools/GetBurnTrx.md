# GetBurnTrx

查询累计销毁的 TRX 数量，不包含转入黑洞账户的金额。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/getburntrx](../../http/node-and-tools/getburntrx.md)。
