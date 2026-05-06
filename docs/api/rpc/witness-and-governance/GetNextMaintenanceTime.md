# GetNextMaintenanceTime

获取下次 SR 维护期开始时间。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetNextMaintenanceTime (EmptyMessage) returns (NumberMessage) {}
```

相似 HTTP 接口见 [/wallet/getnextmaintenancetime](../../http/witness-and-governance/getnextmaintenancetime.md)。
