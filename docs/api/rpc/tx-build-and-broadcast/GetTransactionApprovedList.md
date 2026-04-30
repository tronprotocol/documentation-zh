# GetTransactionApprovedList

返回多签交易当前已签名地址列表（不计算权重，只列签名者）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetTransactionApprovedList (Transaction) returns (TransactionApprovedList) {}
```
