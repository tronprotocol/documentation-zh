# GetTransactionSignWeight

校验已部分签名的多签交易，返回当前权重和是否达到 threshold。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetTransactionSignWeight (Transaction) returns (TransactionSignWeight) {}
```
