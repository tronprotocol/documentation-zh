# GetPaginatedNowWitnessList

分页查询所有 SR 候选人，按当前总票数排序。总票数包含本周期的投票变动，与 [ListWitnesses](ListWitnesses.md) 返回的已存储票数不同。结果不限于 27 位活跃 SR，也不限于 `isJobs=true` 的候选人。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetPaginatedNowWitnessList (PaginatedMessage) returns (WitnessList) {}
```

相似 HTTP 接口见 [/wallet/getpaginatednowwitnesslist](../../http/witness-and-governance/getpaginatednowwitnesslist.md)。
