# GetNodeInfo

获取本节点运行状态、版本、CPU、内存、线程/JVM/操作系统信息、最新区块及对等节点统计信息。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetNodeInfo (EmptyMessage) returns (NodeInfo) {}
```

相似 HTTP 接口见 [/wallet/getnodeinfo](../../http/node-and-tools/getnodeinfo.md)。
