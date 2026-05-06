# net_version

返回当前网络 ID。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getNetVersion`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}'
```

## 响应

值与 [`eth_chainId`](eth_chainId.md) 相同：取 0 号块（创世块）BlockId 的最后 4 字节，hex 编码。主网 / Nile / Shasta 各不相同。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（Nile chainId = `0xcd8690dc`）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0xcd8690dc"
}
```

### 异常响应

同 [`eth_chainId`](eth_chainId.md)：底层取不到创世块时抛 `-32000`，透传底层 `Exception.getMessage()`。
