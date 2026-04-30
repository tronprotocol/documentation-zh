# GetTransactionListFromPending

返回待打包池（pending）中所有交易的 ID 列表。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetTransactionListFromPending (EmptyMessage) returns (TransactionIdList) {}
```
