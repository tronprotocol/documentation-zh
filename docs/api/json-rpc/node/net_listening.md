# net_listening

是否处于 P2P 监听状态。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#isListening`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":1}'
```

## 响应

布尔值。判定逻辑：`nodeInfoService.getNodeInfo().getActiveConnectCount() >= 1`，即至少有 1 个 active 对等连接即视为在监听。

下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": true
}
```

### 异常响应

无。
