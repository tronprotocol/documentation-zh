# eth_protocolVersion

返回最新区块 header 中的协议版本号。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getProtocolVersion`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_protocolVersion","params":[],"id":1}'
```

## 响应

`wallet.getNowBlock().getBlockHeader().getRawData().getVersion()` 的 hex 编码。该字段是 Tron 链协议版本（`BlockHeader.raw_data.version`），与 Ethereum 网络协议版本不同义。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（`0x22` = 34，对应 Nile 当前协议版本）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x22"
}
```

### 异常响应

无。
