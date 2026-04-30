# GetBlock

按区块号或区块哈希查询区块，可选返回完整交易明细。统一替代 `GetNowBlock` / `GetBlockByNum` / `GetBlockById`。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetBlock (BlockReq) returns (BlockExtention) {}
```
