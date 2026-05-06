# GetContractInfo

获取合约的完整运行时信息（包含 runtime code、状态、能量信息）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetContractInfo (BytesMessage) returns (SmartContractDataWrapper) {}
```

相似 HTTP 接口见 [/wallet/getcontractinfo](../../http/smart-contract/getcontractinfo.md)。
