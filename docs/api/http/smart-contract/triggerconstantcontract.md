# /wallet/triggerconstantcontract

只读调用合约（不上链），用于读取 view/pure 函数或预演交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/TriggerConstantContractServlet.java`
- Method：`POST`
- Contract：`protocol.TriggerSmartContract`
- Response：`api.TransactionExtention`
- 支持固化接口：`/walletsolidity/triggerconstantcontract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 调用方地址（合约 `msg.sender`） |
| `contract_address` | string | 是 | 目标合约地址 |
| `function_selector` | string | 否 | 函数签名 |
| `parameter` | string | 否 | ABI 编码参数（hex） |
| `data` | string | 否 | 调用 data（hex），与 `function_selector` 二选一 |
| `call_value` | int64 | 否 | 调用带入的 TRX（sun） |
| `token_id` | int64 | 否 | 调用带入的 TRC-10 token id |
| `call_token_value` | int64 | 否 | 调用带入的 TRC-10 数量 |
| `extra_data` | string | 否 | 交易备注（hex；`visible=true` 时为 UTF-8 文本） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式（响应含 `result.message`，受 `visible` 影响） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/triggerconstantcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "balanceOf(address)",
  "parameter":         "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

`TransactionExtention`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `transaction` | Transaction | 未签名交易（仅作上下文，不应再签名广播） |
| `txid` | string(hex) | 交易哈希 |
| `constant_result` | repeated bytes(hex) | 函数返回值的 ABI 编码 hex；**revert 时是 revert reason 的 ABI 编码**（前 4 字节 `08c379a0` = `Error(string)` 选择器） |
| `result` | Return | 结果状态；revert / `require` 失败时 `result.result=false`，`result.message` 含 `REVERT opcode executed` 或 `runtime error` |
| `energy_used` | int64 | 预估能量消耗 |
| `energy_penalty` | int64 | 能量惩罚（如有） |
| `logs` | repeated TransactionLog | event 日志（如触发） |
| `internal_transactions` | repeated InternalTransaction | 内部调用（如发生） |

响应示例（Nile 实抓）：

```json
{
  "result": { "result": true },
  "energy_used": 935,
  "constant_result": ["0000000000000000000000000000000000000000000000000000000040cfcc00"],
  "transaction": {
    "ret": [{}],
    "visible": false,
    "txID": "cff6488e738ce77f7325572fe0aa2470f87dbf1c95eeeb2c25feec59d5afa35c",
    "raw_data": {
      "contract": [
        {
          "parameter": {
            "value": {
              "data":             "70a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
            },
            "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
          },
          "type": "TriggerSmartContract"
        }
      ],
      "ref_block_bytes": "28c0",
      "ref_block_hash":  "9eabbe133123b34c",
      "expiration":      1777447218000,
      "timestamp":       1777447160779
    },
    "raw_data_hex": "0a0228c022089eabbe133123b34c40d0d6f0c0dd335a8e01081f1289010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412540a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f222470a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f970cb97edc0dd33"
  }
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` 等 ephemeral 字段语义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)。常量调用本身不上链，`transaction` 字段仅作上下文。

### 异常响应

请求进入 servlet 后不会写出 `{"Error": ...}`。由 servlet 接管的异常会被 catch 后写入 `result.code` / `result.message`，HTTP 体仍是 `TransactionExtention`。注意：**EVM revert / runtime 错误不走 `result.code` 路径**，而是 `result.result=true`、`message` 写 revert/runtime 信息，失败标记落在 `transaction.ret[0].ret="FAILED"`。

如果请求体在更早的共享 HTTP 传输层被拒绝，例如超过 `node.http.maxMessageSize`，节点通常会由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large`，而不会进入该 servlet。

| 触发条件 | `result.result` | `result.code` | `result.message` | 其他 |
|---|---|---|---|---|
| `contract_address` 已设置但合约不存在 | 缺省 (false) | `CONTRACT_VALIDATE_ERROR` | `Smart contract is not exist.` | — |
| 节点关闭 constant-call 支持 | 缺省 (false) | `CONTRACT_VALIDATE_ERROR` | `this node does not support constant` | — |
| EVM revert / `require` 失败 | true | 缺省（`SUCCESS`，不出现） | `REVERT opcode executed` | `transaction.ret[0].ret="FAILED"`；`constant_result[0]` 为 `Error(string)` 的 ABI 编码（合约带 reason 时） |
| EVM 运行时错误（OOG、非法指令等，无 `result.getException()`） | true | 缺省（`SUCCESS`，不出现） | `result.getRuntimeError()` 原始字符串 | 同上 |
| `result.getException() != null`（如 `OutOfTimeException`） | 缺省 (false) | `OTHER_ERROR` | `<exceptionClass> : <message>`（`"` → `'`） | — |
| 其他（hex 解析、参数缺失、proto merge 等） | 缺省 (false) | `OTHER_ERROR` | `<exceptionClass> : <message>`（`"` → `'`） | — |

revert 时 `result.message` 不携带原 reason 字符串；reason 需自己解码 `constant_result[0]`：跳过前 4 字节选择器 `08c379a0`，按 ABI `string` 解码剩余数据。
