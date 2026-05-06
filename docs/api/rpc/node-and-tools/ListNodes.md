# ListNodes

列出节点已发现的对等节点。

- 服务：仅支持 `Wallet`

```protobuf
rpc ListNodes (EmptyMessage) returns (NodeList) {}
```

相似 HTTP 接口见 [/wallet/listnodes](../../http/node-and-tools/listnodes.md)。
