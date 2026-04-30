# GetBlockByLimitNext2

获取区间 `[startNum, endNum)` 的区块列表（不包含 endNum）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetBlockByLimitNext2 (BlockLimit) returns (BlockListExtention) {}
```

相似 HTTP 接口见 [/wallet/getblockbylimitnext](../../http/block-and-tx-query/getblockbylimitnext.md)。
