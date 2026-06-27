# UnfreezeAsset2

解冻发行方在 `frozen_supply` 中冻结的 token 份额（仅 TRC-10 发行方调用，到期后才能成功）。

- 服务：仅支持 `Wallet`

```protobuf
rpc UnfreezeAsset2 (UnfreezeAssetContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/unfreezeasset](../../http/asset/unfreezeasset.md)。
