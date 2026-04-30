# eth_call

只读调用智能合约（不上链、不消耗 energy）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getCall`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | object | 是 | `CallArguments` 对象，见下表 |
| `params[1]` | string \| object | 是 | 区块标识：tag 字符串、或 `{"blockNumber": "0x..."}` / `{"blockHash": "0x..."}` 对象（EIP-1898）。**仅支持 `latest`**（其它 tag 抛错；具体高度即便存在也会被拒绝） |

`CallArguments` 字段（`framework/src/main/java/org/tron/core/services/jsonrpc/types/CallArguments.java`）：

| 字段 | 默认值 | 说明 |
|---|---|---|
| `from` | `0x0000000000000000000000000000000000000000` | 调用者地址 |
| `to` | 必填 | 合约地址 |
| `value` | `""` | 转入合约的 callValue（sun，hex） |
| `data` | `null` | calldata（4 字节 selector + abi.encode 参数） |
| `gas` / `gasPrice` / `nonce` | 不使用 | — |

```bash
# 例：调用 Nile testnet 上 Tether USD（USDT）的 symbol() 函数
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_call",
    "params":[{
      "to":"0xeca9bc828a3005b9a3b909f2cc5c2a54794de05f",
      "data":"0x95d89b41"
    },"latest"]
  }'
```

## 响应

合约 `view` / `pure` 函数的返回值（拼接所有 `constantResult` 段），hex 编码。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（USDT 的 `symbol()` 返回 ABI 编码后的字符串 `"USDT"`：偏移 `0x20` + 长度 `0x4` + UTF-8 字节 `5553445400...`）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000045553445400000000000000000000000000000000000000000000000000000000"
}
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[1]` 既不是 string 也不是 object | `-32600` | `invalid json request` |
| `params[1]` object 形式中 `blockNumber` / `blockHash` 都缺失 | `-32600` | `invalid json request` |
| `params[1]` 中 `blockNumber` 不是合法 hex | `-32602` | `invalid block number` |
| `params[1]` 中指定的块不存在 | `-32000` | `header not found` 或 `header for hash not found` |
| `params[1]` tag 是 `earliest` / `pending` / `finalized` | `-32602` | `TAG [earliest \| pending \| finalized] not supported` |
| `params[1]` 是具体 hex 高度（即便有效） | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `from` / `to` 地址非法 | `-32602` | 透传 message |
| `value` 不是合法 hex | `-32602` | `invalid param value: invalid hex number` |
| 合约校验失败（如 `to` 非合约、参数不匹配等） | `-32600` | `ContractValidateException` 透传 message（无 message 时 fallback `Contract validate error : `） |
| EVM 执行 `REVERT` | `-32000` | message + （若 revert 数据以 `Error(string)` 选择器开头）解析后的字符串；`error.data` 携带原始 revert hex |
| 其他执行/编码错误 | `-32000` | 透传 message（双引号被替换为单引号） |
