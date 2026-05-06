# /wallet/triggersmartcontract

触发智能合约（写交易）。返回未签名交易和预执行结果。

- 源码：`framework/src/main/java/org/tron/core/services/http/TriggerSmartContractServlet.java`
- Method：`POST`
- Contract：`protocol.TriggerSmartContract`
- Response：`api.TransactionExtention`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 调用方地址 |
| `contract_address` | string | 是 | 目标合约地址 |
| `function_selector` | string | 否 | 函数签名（如 `transfer(address,uint256)`），与 `parameter` 配套 |
| `parameter` | string | 否 | ABI 编码的参数（hex，无函数选择子） |
| `data` | string | 否 | 直接给定调用 data（hex），与 `function_selector` 二选一 |
| `call_value` | int64 | 否 | 调用带入的 TRX（sun） |
| `token_id` | int64 | 否 | 调用带入 TRC10 token id |
| `call_token_value` | int64 | 否 | 调用带入 TRC10 数量 |
| `fee_limit` | int64 | 是 | 交易费用上限（sun） |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式（响应含 `result.message`，受 `visible` 影响） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/triggersmartcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "transfer(address,uint256)",
  "parameter":         "000000000000000000000000088a2bfcb1c7271029fd69a66859d555608958840000000000000000000000000000000000000000000000000000000000000064",
  "fee_limit":  100000000,
  "call_value": 0
}
'
```

## 响应

`TransactionExtention`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `transaction` | Transaction | 未签名交易 |
| `txid` | string(hex) | 交易哈希 |
| `constant_result` | repeated bytes(hex) | 仅在被 ABI 识别为 `view` / `pure` 函数时填充（写交易通常无此字段） |
| `result` | Return | 结果状态 |
| `energy_used` | int64 | 仅在常量调用路径填充；普通写交易不返回 |
| `energy_penalty` | int64 | 能量惩罚（如有） |

响应示例（Nile 实抓）：

```json
{
  "result": { "result": true },
  "transaction": {
    "visible": false,
    "txID": "8c621a0dc9bd4d405b20d0a43143955b9f546f98bbfde1aec295a65b0f925629",
    "raw_data": {
      "contract": [
        {
          "parameter": {
            "value": {
              "data":             "a9059cbb000000000000000000000000088a2bfcb1c7271029fd69a66859d5556089588400000000000000000000000000000000000000000000000000000000000000064",
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
            },
            "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
          },
          "type": "TriggerSmartContract"
        }
      ],
      "ref_block_bytes": "28c3",
      "ref_block_hash":  "ce6d340282788569",
      "fee_limit":       100000000,
      "expiration":      1777447227000,
      "timestamp":       1777447168009
    },
    "raw_data_hex": "0a0228c32208ce6d34028278856940f89cf1c0dd335aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f2244a9059cbb000000000000000000000000088a2bfcb1c7271029fd69a66859d5556089588400000000000000000000000000000000000000000000000000000000000000647089d0edc0dd33900180c2d72f"
  }
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` 等 ephemeral 字段语义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)。写交易路径不会填充 `txid` / `constant_result` / `energy_used`；如需要预演结果改用 [`/wallet/triggerconstantcontract`](triggerconstantcontract.md)。

> 仅做预演（不上链）请用 [`/wallet/triggerconstantcontract`](triggerconstantcontract.md)；仅估算能量请用 [`/wallet/estimateenergy`](estimateenergy.md)。

### 异常响应

不会写出 `{"Error": ...}`。所有异常被 catch 后写入 `result.code`、`result.message`，HTTP 体仍是 `TransactionExtention`：

| 触发条件 | `result.result` | `result.code` | `result.message` |
|---|---|---|---|
| `owner_address` / `contract_address` 为空（`InvalidParameterException`） | false | `OTHER_ERROR` | `class java.security.InvalidParameterException : owner_address isn't set.` 等 |
| 合约校验失败 / fee_limit 超限 / 调用账户不存在等（`ContractValidateException`） | false | `CONTRACT_VALIDATE_ERROR` | 校验器原始描述 |
| 其他（hex 解析、proto merge 等） | false | `OTHER_ERROR` | `<exceptionClass> : <message>`（`"` → `'`） |
