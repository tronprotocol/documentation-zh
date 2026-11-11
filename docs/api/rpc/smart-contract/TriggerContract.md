# TriggerContract

构造未签名的智能合约交易，并返回构造状态。当合约的链上 ABI 将函数标记为 `view` 或 `pure`，或将旧版 `constant` 标志设为 `true` 时，此方法会执行 constant call 并返回模拟结果。模拟普通的状态变更调用请使用 [TriggerConstantContract](TriggerConstantContract.md)。

- 服务：仅支持 `Wallet`

```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/triggersmartcontract](../../http/smart-contract/triggersmartcontract.md)。
