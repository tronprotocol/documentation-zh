# GetContract

按合约地址获取合约元信息。返回 `SmartContract` 本体（含 deploy 时的 `bytecode`），但**不含运行时码 `runtimecode` 与 `contract_state`**。如需运行时信息，请用 `GetContractInfo`。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetContract (BytesMessage) returns (SmartContract) {}
```
