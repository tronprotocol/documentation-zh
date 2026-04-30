# TriggerConstantContract

只读调用合约（不上链），用于读取 view/pure 函数或预演交易。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc TriggerConstantContract (TriggerSmartContract) returns (TransactionExtention) {}
```
