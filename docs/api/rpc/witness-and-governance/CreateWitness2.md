# CreateWitness2

申请成为超级代表候选人。费用由当前链参数 `getAccountUpgradeCost` 决定，单位为 sun；默认值为 9,999,000,000 sun（9999 TRX），可通过治理提案修改。

- 服务：仅支持 `Wallet`

```protobuf
rpc CreateWitness2 (WitnessCreateContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/createwitness](../../http/witness-and-governance/createwitness.md)。
