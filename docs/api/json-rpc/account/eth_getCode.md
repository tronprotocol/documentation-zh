# eth_getCode

查询合约 runtime 字节码。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getABIOfSmartContract`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 合约地址：20 字节 hex，或以 `41` 开头的 21 字节 Tron hex；均可带或不带 `0x`（不接受 base58check） |
| `params[1]` | string | 是 | 区块标识，**仅支持 `latest`** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getCode","params":["0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825","latest"],"id":1}'
```

## 响应

`SmartContractDataWrapper.runtimecode` 的 hex 编码（`0x` 前缀）。地址不是合约或合约不存在返回 `0x`。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（该地址是 ERC-1167 minimal proxy clone，实现合约嵌在字节码中部）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x363d3d373d3d3d363d73337d2c535241e1bc38e9c1fc2181843aef31dfaa5af43d82803e903d91602b57fd5bf30000000000000000000000003804c9c36c304d3d3d40bcc1a7c8d47591eda1b0"
}
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[1]` 是 `earliest` / `pending` / `finalized` / `safe` | `-32602` | `TAG [earliest \| pending \| finalized \| safe] not supported` |
| `params[1]` 是合法 hex 或十进制数字 | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[1]` 既不是合法 tag，也不是合法的非负 hex/十进制数字 | `-32602` | `invalid block number` |
| `params[0]` 不是合法地址 | `-32602` | 透传 message |
