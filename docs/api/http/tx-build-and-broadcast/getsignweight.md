# /wallet/getsignweight

校验已部分签名的多签交易，返回当前权重和是否达到 threshold。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionSignWeightServlet.java`
- Method：`POST`
- Response：`api.TransactionSignWeight`（`api.proto`）

## 请求参数

直接传 `protocol.Transaction` 的 JSON（含已收集到的若干 `signature`）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` | object | 是 | 与 createtransaction 返回一致 |
| `raw_data_hex` | string | 否（节点忽略） | 同 [`broadcasttransaction`](broadcasttransaction.md)：客户端可视化辅助字段，不参与验签 |
| `signature` | string[] | 否 | 已收集的签名；省略时仍可解析请求，`current_weight` 保持为 `0` |
| `visible` | bool | 否 | 控制地址及 bytes 字段的格式；`result.message` 是 protobuf string，无论 `visible` 取值如何，均保持为 JSON 文本 |

示例：请求体为带 `signature` 的 Transaction JSON，结构同 [`/wallet/broadcasttransaction`](broadcasttransaction.md)。

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getsignweight \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "raw_data":     { "...": "..." },
  "raw_data_hex": "0a02...",
  "signature":    ["b8c0...01"]
}
'
```

> 上例为占位结构。实际权重计算通常使用已签名的多签交易 JSON，但该接口也接受空的或省略的 `signature` 数组，并在权限结果中报告 `current_weight=0`。

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `permission` | Permission | 当前生效的权限 |
| `current_weight` | int64 | 当前已累积权重 |
| `result.code` | enum | `ENOUGH_PERMISSION` / `NOT_ENOUGH_PERMISSION` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `PERMISSION_ERROR` / `OTHER_ERROR` |
| `result.message` | string | 错误描述，始终为 JSON 文本，不受 `visible` 影响 |
| `transaction` | TransactionExtention | 提交的交易及其已收集的签名 |
| `approved_list` | repeated bytes | `visible=true` 时为 base58 地址数组，`visible=false` 时为 hex（21 字节，带 `41` 前缀） |

响应示例：

```json
{
  "permission": {
    "type":            "Active",
    "id":              2,
    "permission_name": "active",
    "threshold":       2,
    "keys": [
      { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 },
      { "address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a", "weight": 1 }
    ]
  },
  "current_weight": 1,
  "approved_list":  ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":         { "code": "NOT_ENOUGH_PERMISSION" },
  "transaction": {
    "txid":        "<由 raw_data 计算>",
    "result":      { "result": true },
    "transaction": { "...": "..." }
  }
}
```

当 `current_weight >= permission.threshold` 时，结果码为 `ENOUGH_PERMISSION`（默认枚举值，在 JSON 中省略）。这仅确认已达到所选权限的签名阈值；广播时仍会检查签名长度、TAPOS、过期时间和交易有效性。

> 注意：交易 JSON 解码后，签名格式、地址恢复和权限检查失败会写入响应的 `result.code` / `result.message`（HTTP 200）。下表列出返回 `{"Error": ...}` 形式响应的情况，包括 JSON 解码阶段的非法签名 hex。

protobuf JSON 解析器也接受将单个 hex 字符串作为 `signature`，并将其视为仅含一个元素的列表；非数组值不一定导致解析错误。正常请求请使用文档规定的数组形式。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| `raw_data` / `raw_data.contract` 缺失或为 null | 访问缺失的对象或数组时返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| `raw_data` 不是对象，或 `raw_data.contract` 不是数组（不包括能解析为所需结构的 JSON 字符串） | `{"Error": "class org.tron.json.JSONException : <message>"}`，例如 `Field 'contract' is not an array` |
| 签名 hex 非法，或 `raw_data` 中的字段值无法由 `JsonFormat.merge` 解码 | `packTransaction` 捕获最终的 `JsonFormat$ParseException` 并返回 `null`，下游操作随后返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
