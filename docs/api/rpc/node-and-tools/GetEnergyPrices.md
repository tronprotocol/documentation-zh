# GetEnergyPrices

获取历史能量单价（每次提案变更后追加）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetEnergyPrices (EmptyMessage) returns (PricesResponseMessage) {}
```

相似 HTTP 接口见 [/wallet/getenergyprices](../../http/node-and-tools/getenergyprices.md)。
