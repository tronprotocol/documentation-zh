# eth_chainId

返回链 ID。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethChainId`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

## 响应

取 0 号块（创世块）BlockId 字节流的**最后 4 字节**，hex 编码。每个链各有独立常量值，常见参考：

| 网络 | chainId |
|---|---|
| Mainnet | `0x2b6653dc` |
| Nile testnet | `0xcd8690dc` |
| Shasta testnet | `0x94a9059e` |

下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0xcd8690dc"
}
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 无法取到 0 号块（节点未完成创世块加载等极端情况） | `-32000` | 透传底层 `Exception.getMessage()` |
