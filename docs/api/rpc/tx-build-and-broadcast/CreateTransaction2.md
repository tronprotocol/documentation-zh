# CreateTransaction2

创建一笔 TRX 转账（`TransferContract`）的未签名交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc CreateTransaction2 (TransferContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/createtransaction](../../http/tx-build-and-broadcast/createtransaction.md)。
