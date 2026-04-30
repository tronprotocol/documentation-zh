# GetBurnTrx

查询累计销毁的 TRX 数量（包括手续费、合约销毁等）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}
```
