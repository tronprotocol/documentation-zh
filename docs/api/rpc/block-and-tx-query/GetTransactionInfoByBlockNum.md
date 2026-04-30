# GetTransactionInfoByBlockNum

按区块号返回该区块所有交易的 `TransactionInfo`（执行结果）数组。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetTransactionInfoByBlockNum (NumberMessage) returns (TransactionInfoList) {}
```
