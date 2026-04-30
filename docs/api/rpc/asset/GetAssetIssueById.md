# GetAssetIssueById

按 token id 查询 TRC10（推荐方式，token id 全局唯一）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetAssetIssueById (BytesMessage) returns (AssetIssueContract) {}
```
