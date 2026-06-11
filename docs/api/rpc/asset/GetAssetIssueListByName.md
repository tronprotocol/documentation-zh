# GetAssetIssueListByName

按 token 名查询所有同名 TRC10。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetAssetIssueListByName (BytesMessage) returns (AssetIssueList) {}
```

相似 HTTP 接口见 [/wallet/getassetissuelistbyname](../../http/asset/getassetissuelistbyname.md)。
