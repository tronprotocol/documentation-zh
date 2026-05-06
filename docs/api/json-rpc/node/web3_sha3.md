# web3_sha3

计算输入数据的 Keccak-256 hash。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#web3Sha3`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 待哈希的字节流，hex 编码（带或不带 `0x` 前缀均可） |

请求示例：

```bash
# 例：对 ASCII 字符串 "hello" 求 Keccak-256
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"web3_sha3","params":["0x68656c6c6f"],"id":1}'
```

## 响应

`0x` 前缀的 32 字节 hex（即 Keccak-256，与 EVM `KECCAK256` 一致；**不是** SHA3-256）。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（`keccak256("hello") = 1c8aff95...deac8`）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8"
}
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 不是合法 hex | `-32602` | `invalid input value` |
