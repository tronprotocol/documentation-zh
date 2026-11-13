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

`wallet.getCoinbase()` 返回的字符串。节点必须以 witness 模式运行（`isWitness=true`），且从其配置的本地 witness 私钥派生出的地址中，至少有一个存在于链上的 witness 列表中。返回第一个匹配的本地地址。有匹配地址时，响应示例如下：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c" }
```

> 注：这里的 21 字节（`0x41` + 20 字节）是 Tron 原生地址格式，与标准以太坊 20 字节不同。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 节点未以 witness 模式运行，或其本地 witness 私钥派生出的地址均不在链上的 witness 列表中 | `-32000` | `etherbase must be explicitly specified` |

下例为上面 curl 调用 Nile testnet 抓回的真实响应（提供服务的节点没有返回匹配的 witness 地址，因此走异常分支）：

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
