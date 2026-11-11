# GetTransactionApprovedList

根据账户当前权限验证全部签名后，返回交易的签名地址。验证失败时返回错误，不返回已批准地址列表。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetTransactionApprovedList (Transaction) returns (TransactionApprovedList) {}
```

相似 HTTP 接口见 [/wallet/getapprovedlist](../../http/tx-build-and-broadcast/getapprovedlist.md)。
