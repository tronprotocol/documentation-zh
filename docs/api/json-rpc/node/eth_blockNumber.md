# eth_blockNumber

最新区块高度。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getLatestBlockNum`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## 响应

`wallet.getNowBlock().getBlockHeader().getRawData().getNumber()` 的 hex 编码。Solidity 端口返回固化块的高度。

下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x3fe1dec"
}
```

> 该值随每个新块前进，再次请求会得到更高的值。

### 异常响应

无。
