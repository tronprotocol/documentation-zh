# GetTransactionCountByBlockNum

返回某区块号包含的交易数。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetTransactionCountByBlockNum (NumberMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/gettransactioncountbyblocknum](../../http/block-and-tx-query/gettransactioncountbyblocknum.md)。
