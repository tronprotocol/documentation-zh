# GetTransactionInfoById

按交易 ID 查询**执行结果**（包含 receipt、log、内部调用、资源消耗）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetTransactionInfoById (BytesMessage) returns (TransactionInfo) {}
```
