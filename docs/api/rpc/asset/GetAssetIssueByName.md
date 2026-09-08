# GetAssetIssueByName

按 token 名查询单个 TRC-10。**注意**：自 `ALLOW_SAME_TOKEN_NAME` 提案后，name 不再唯一，调用此接口在重名时会报错；推荐用 `GetAssetIssueById` 或 `GetAssetIssueListByName`。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetAssetIssueByName (BytesMessage) returns (AssetIssueContract) {}
```

相似 HTTP 接口见 [/wallet/getassetissuebyname](../../http/asset/getassetissuebyname.md)。
