# GetBlockById

按区块哈希查询区块。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetBlockById (BytesMessage) returns (Block) {}
```

相似 HTTP 接口见 [/wallet/getblockbyid](../../http/block-and-tx-query/getblockbyid.md)。
