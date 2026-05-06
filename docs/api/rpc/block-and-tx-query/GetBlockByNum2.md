# GetBlockByNum2

按区块号查询区块。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetBlockByNum2 (NumberMessage) returns (BlockExtention) {}
```

相似 HTTP 接口见 [/wallet/getblockbynum](../../http/block-and-tx-query/getblockbynum.md)。
