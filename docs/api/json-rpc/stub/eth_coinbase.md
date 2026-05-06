# eth_coinbase

返回 etherbase 地址（兼容 Ethereum 客户端，Tron 自身没有 PoW coinbase 概念）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getCoinbase`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_coinbase","params":[],"id":1}'
```

## 响应

`wallet.getCoinbase()` 返回的字符串。仅在节点显式配置 `node.etherbase` 时有值。配置后的响应形如：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c" }
```

> 注：这里的 21 字节（`0x41` + 20 字节）是 Tron 原生地址格式，与标准以太坊 20 字节不同。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 节点未配置 etherbase | `-32000` | `etherbase must be explicitly specified` |

下例为上面 curl 调用 Nile testnet 抓回的真实响应（`nile.trongrid.io` 未配置 etherbase，因此走异常分支）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,
    "message": "etherbase must be explicitly specified",
    "data": "{}"
  }
}
```
