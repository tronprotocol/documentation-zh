# eth_getBalance

查询账户 TRX 余额。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTrxBalance`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 账户地址。20 字节 hex（带或不带 `0x`）或 base58check（如 `T...`） |
| `params[1]` | string | 是 | 区块标识，**仅支持 `latest`** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xdd791d6b49e190062d650e6a23c575510d35f2f9","latest"],"id":1}'
```

## 响应

余额（sun）的 hex 编码；账户不存在视为 0。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（`0x6d1a6c48` ≈ 1.83 TRX）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x6d1a6c48" }
```

> 余额是实时数据，再次请求会随账户活动变化。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[1]` 是 `earliest` / `pending` / `finalized` / `safe` | `-32602` | `TAG [earliest \| pending \| finalized \| safe] not supported` |
| `params[1]` 是合法 hex 数字（具体高度） | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[1]` 既不是合法 tag 也不是合法 hex | `-32602` | `invalid block number` |
| `params[0]` 不是合法地址 | `-32602` | 透传 `addressCompatibleToByteArray` 抛出的 message |

> Tron 不支持任意历史块的状态查询，因此即使传具体高度也会被显式拒绝。
