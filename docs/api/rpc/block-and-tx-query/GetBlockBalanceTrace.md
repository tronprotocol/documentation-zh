# GetBlockBalanceTrace

返回某区块内所有交易引发的余额变动追踪（block balance trace）。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}
```
