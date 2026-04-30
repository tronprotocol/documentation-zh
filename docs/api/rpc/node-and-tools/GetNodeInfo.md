# GetNodeInfo

获取本节点运行状态、版本、内存、磁盘、最新区块、对等节点统计等信息。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetNodeInfo (EmptyMessage) returns (NodeInfo) {}
```
