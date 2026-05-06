# EstimateEnergy

预估调用合约所需能量。需节点开启 `vm.estimateEnergy=true`。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc EstimateEnergy (TriggerSmartContract) returns (EstimateEnergyMessage) {}
```

相似 HTTP 接口见 [/wallet/estimateenergy](../../http/smart-contract/estimateenergy.md)。
