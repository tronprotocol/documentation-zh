# eth_getWork

兼容方法。返回 `[currentBlockHash, null, null]` —— 仅前 1 项有意义（当前最新块 hash），其余两项常量 `null`。Tron 没有 PoW work、target、seed 概念。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetWork`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getWork","params":[],"id":1}'
```

## 响应

3 元素数组。下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    "0x0000000003fe2429fd471ebb02f925accea59aa1d2ee593ebcba6596204e1c18",
    null,
    null
  ]
}
```

> 第 1 项是请求时刻的最新块 hash，会随每个新块变化；节点尚未生成区块时该项为 `null`。

### 异常响应

无。
