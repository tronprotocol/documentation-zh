# UpdateAsset2

修改 TRC10 token 的描述、URL 及带宽限额（仅发行方）。

- 服务：仅支持 `Wallet`

```protobuf
rpc UpdateAsset2 (UpdateAssetContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/updateasset](../../http/asset/updateasset.md)。
