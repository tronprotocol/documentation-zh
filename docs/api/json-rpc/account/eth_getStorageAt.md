# eth_getStorageAt

查询合约存储槽（slot）的值。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getStorageAt`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 合约地址：20 字节 hex，或以 `41` 开头的 21 字节 Tron hex；均可带或不带 `0x`（不接受 base58check） |
| `params[1]` | string | 是 | 存储槽索引，带或不带 `0x` 的 hex 编码；短于 32 字节时在左侧补 `0` |
| `params[2]` | string | 是 | 区块标识，**仅支持 `latest`** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getStorageAt","params":["0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825","0x0","latest"],"id":1}'
```

## 响应

槽位的 32 字节值，hex 编码。**地址不是合约**或槽位未写入时返回 32 字节 0。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（合约 slot 0 存的 `uint256` 计数器值为 `0x8`）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x0000000000000000000000000000000000000000000000000000000000000008" }
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[2]` 是 `earliest` / `pending` / `finalized` / `safe` | `-32602` | `TAG [earliest \| pending \| finalized \| safe] not supported` |
| `params[2]` 是合法 hex 或十进制数字 | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[2]` 既不是合法 tag，也不是合法的非负 hex/十进制数字 | `-32602` | `invalid block number` |
| `params[0]` 不是合法地址 | `-32602` | 透传 message |
| `params[1]` 为 null、过长，或无法解码为合法 storage key | `-32602` | `invalid storage key value` |
