# GetTransactionFromPending

从待打包池（pending）按交易 ID 取交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetTransactionFromPending (BytesMessage) returns (Transaction) {}
```

相似 HTTP 接口见 [/wallet/gettransactionfrompending](../../http/block-and-tx-query/gettransactionfrompending.md)。
