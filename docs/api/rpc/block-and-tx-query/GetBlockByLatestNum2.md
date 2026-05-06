# GetBlockByLatestNum2

获取最新的 N 个区块。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetBlockByLatestNum2 (NumberMessage) returns (BlockListExtention) {}
```

相似 HTTP 接口见 [/wallet/getblockbylatestnum](../../http/block-and-tx-query/getblockbylatestnum.md)。
