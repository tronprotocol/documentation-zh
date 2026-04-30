# GetContractInfo

获取合约的完整运行时信息（包含 runtime code、状态、能量信息）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetContractInfo (BytesMessage) returns (SmartContractDataWrapper) {}
```
