# net_peerCount

对等节点数量。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getPeerCount`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1}'
```

## 响应

`nodeInfoService.getNodeInfo().getPeerList().size()` 的 hex 编码（**包含全部 peer，不仅限于 active**）。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（`0x3b` = 59 个 peer）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x3b"
}
```

> peer 数随网络拓扑实时变化，再次请求会得到不同的值。

### 异常响应

无。
