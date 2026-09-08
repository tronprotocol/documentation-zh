# GetPaginatedAssetIssueList

按分页查询全网 TRC-10 token。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetPaginatedAssetIssueList (PaginatedMessage) returns (AssetIssueList) {}
```

相似 HTTP 接口见 [/wallet/getpaginatedassetissuelist](../../http/asset/getpaginatedassetissuelist.md)。
