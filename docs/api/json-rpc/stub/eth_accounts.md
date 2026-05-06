# eth_accounts

兼容方法。Tron 节点不托管账户私钥，恒返回空数组。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getAccounts`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}'
```

## 响应

恒为空数组。下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{ "jsonrpc": "2.0", "id": 1, "result": [] }
```

### 异常响应

无。
