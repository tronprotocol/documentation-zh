# GetTransactionById

按 txID 查询交易，包括 `ret[].contractRet` 中的基本执行状态。回执、日志和内部交易等详细执行信息，请使用 [`GetTransactionInfoById`](GetTransactionInfoById.md) 查询。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetTransactionById (BytesMessage) returns (Transaction) {}
```

相似 HTTP 接口见 [/wallet/gettransactionbyid](../../http/block-and-tx-query/gettransactionbyid.md)。
