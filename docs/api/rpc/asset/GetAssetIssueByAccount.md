# GetAssetIssueByAccount

查询某账户作为发行方发行的所有 TRC-10。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetAssetIssueByAccount (Account) returns (AssetIssueList) {}
```

相似 HTTP 接口见 [/wallet/getassetissuebyaccount](../../http/asset/getassetissuebyaccount.md)。
