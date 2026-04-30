# /wallet/getsignweight

校验已部分签名的多签交易，返回当前权重和是否达到 threshold。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionSignWeightServlet.java`
- Method：`POST`
- Response：`api.TransactionSignWeight`（`api.proto:1259`）

## 请求参数

直接传 `protocol.Transaction` 的 JSON（含已收集到的若干 `signature`）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` / `raw_data_hex` | object/string | 是 | 同 broadcasttransaction |
| `signature` | string[] | 是 | 已收集的签名（可以只有 1 个） |
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

> 上例为占位结构；实际请求体应为带至少一个 `signature` 的多签交易 JSON。

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
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `raw_data_hex` 不是合法 hex | `{"Error": "class java.lang.NullPointerException : <message>"}`（`Util.packTransaction` 捕获 `JsonFormat$ParseException` 后返 `null`，下游空指针） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
