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
| `visible` | bool | 否 | 地址、文本字段格式（响应含 `result.message`，受 `visible` 影响） |

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
| `result.message` | string | 错误描述 |
| `transaction` | TransactionExtention | 原交易；其中 `transaction.transaction` 字段经 `Util.printTransactionToJSON` 重写为完整未签名交易 JSON（含 `txID`、`raw_data.contract`、`raw_data_hex`） |
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
    "transaction": { "...": "..." }
  }
}
```

`current_weight >= permission.threshold` 时 `code=ENOUGH_PERMISSION`，可以广播。

> 注意：签名解析、地址恢复、权限不足等错误**不会**走 `Util.processError`，而是写入响应体的 `result.code` / `result.message` 字段（HTTP 200）。下表只列出导致 `{"Error": ...}` 形式响应的故障。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| 缺少 `raw_data`、`raw_data.contract` 不是数组、`signature` 非数组或元素非 hex、`raw_data` 字段类型不符等 | `{"Error": "class java.lang.NullPointerException : null"}`（`Util.packTransaction` 把 `JsonFormat$ParseException` / `ClassCastException` 静默捕获后返回 `null`，下游 `getTransactionSignWeight(null)` 触发空指针） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
