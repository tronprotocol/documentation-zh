# TriggerContract

触发智能合约（写交易）。返回未签名交易和预执行结果。

- 服务：仅支持 `Wallet`

```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```
