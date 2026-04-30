# BroadcastTransaction

广播一笔已签名的交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc BroadcastTransaction (Transaction) returns (Return) {}
```

相似 HTTP 接口见 [/wallet/broadcasttransaction](../../http/tx-build-and-broadcast/broadcasttransaction.md)。
