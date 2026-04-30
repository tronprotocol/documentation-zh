# GetPendingSize

返回当前节点 pending 池中的交易数量。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetPendingSize (EmptyMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/getpendingsize](../../http/block-and-tx-query/getpendingsize.md)。
