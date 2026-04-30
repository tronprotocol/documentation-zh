# GetTransactionById

按交易 ID 查询交易（**不含执行结果**，只返回打包前的交易体）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetTransactionById (BytesMessage) returns (Transaction) {}
```
