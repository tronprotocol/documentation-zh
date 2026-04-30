# /wallet/getapprovedlist

返回多签交易当前已签名地址列表（不计算权重，只列签名者）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionApprovedListServlet.java`
- Method：`POST`
- Response：`api.TransactionApprovedList`（`api.proto:1280`）

## 请求参数

请求体同 [`/wallet/getsignweight`](getsignweight.md)：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` / `raw_data_hex` | object/string | 是 | Transaction |
| `signature` | string[] | 是 | 已收集的签名 |
| `visible` | bool | 否 | 地址、文本字段格式（响应含 `result.message`，受 `visible` 影响） |

示例：请求体为带 `signature` 的 Transaction JSON，结构同 [`/wallet/broadcasttransaction`](broadcasttransaction.md)。

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getapprovedlist \
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

> 上例为占位结构；实际请求体应为带至少一个 `signature` 的多签交易 JSON（来自 [`/wallet/createtransaction`](createtransaction.md) 等并加签）。

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `approved_list` | repeated bytes | 已签名地址；`visible=true` 时为 base58 数组，`visible=false` 时为 hex（21 字节，带 `41` 前缀） |
| `result.code` | enum | `SUCCESS` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `OTHER_ERROR` |
| `result.message` | string | 错误描述（`visible=true` 时 UTF-8，否则 hex） |
| `transaction` | TransactionExtention | 原交易；其中 `transaction.transaction` 经 `Util.printTransactionToJSON` 重写为完整未签名交易 JSON（含 `txID`、`raw_data.contract`、`raw_data_hex`） |

响应示例：

```json
{
  "approved_list": ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":       { "code": "SUCCESS" },
  "transaction": {
    "txid":        "<由 raw_data 计算>",
    "transaction": { "...": "..." }
  }
}
```

> 注意：签名解析、地址恢复等错误**不会**走 `Util.processError`，而是写入响应体的 `result.code` / `result.message` 字段（HTTP 200）。下表只列出导致 `{"Error": ...}` 形式响应的故障。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `raw_data_hex` 不是合法 hex | `{"Error": "class java.lang.NullPointerException : <message>"}`（`Util.packTransaction` 捕获 `JsonFormat$ParseException` 后返 `null`，下游空指针） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
