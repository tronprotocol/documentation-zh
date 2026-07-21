# /wallet/getapprovedlist

返回多签交易当前已签名地址列表（不计算权重，只列签名者）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionApprovedListServlet.java`
- Method：`POST`
- Response：`api.TransactionApprovedList`（`api.proto`）

## 请求参数

请求体同 [`/wallet/getsignweight`](getsignweight.md)：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` | object | 是 | 与 createtransaction 返回一致 |
| `raw_data_hex` | string | 否（节点忽略） | 同 [`broadcasttransaction`](broadcasttransaction.md)：客户端可视化辅助字段，不参与验签 |
| `signature` | string[] | 否 | 已收集的签名；省略时仍可解析请求，已批准地址列表为空 |
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

> 上例为占位结构。实际权限检查通常使用由 [`/wallet/createtransaction`](createtransaction.md) 等接口生成并加签的多签交易 JSON，但该接口也接受空的或省略的 `signature` 数组，并返回空的已批准地址列表。

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
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| 缺少 `raw_data`、`raw_data.contract` 不是数组、`signature` 非数组或元素非 hex、`raw_data` 字段类型不符等 | `{"Error": "class java.lang.NullPointerException : null"}`（`Util.packTransaction` 把 `JsonFormat$ParseException` / `ClassCastException` 静默捕获后返回 `null`，下游 `getTransactionApprovedList(null)` 触发空指针） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
